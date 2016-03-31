from ControlData import *
from DebugData import *
from threading import Thread,Event
import time

class TimerThread(Thread): 
    def __init__(self, handler, interval): 
        Thread.__init__(self) 
        self.stopped = Event()
        self.handler = handler
        self.interval = interval 
 
    def run(self): 
        while not self.stopped.wait(self.interval):
            if self.stopped.isSet():
                print "> Breaking thread"
                break
            self.handler() 

    def stop(self):
        self.stopped.set()

class DroneControler:
    usartConnection = None
    ipConnection = None
    
    controlData = None
    debugData = None

    maxTimeoutCounter = 20 # 20 * 0.05 = 1s
    timeoutCounter = 0

    def __init__(self, usartConnection):
        self.usartConnection = usartConnection
        self.sendingThread = TimerThread(self.send, 0.05)
        self.receivingThread = TimerThread(self.receive, 0.05)
        
    def setIpConnection(self, ipConnection):
        self.ipConnection = ipConnection

    def enable(self):
        self.sendingThread.start()
        self.receivingThread.start()
        
    def disable(self):
        self.sendingThread.stop()
        self.receivingThread.stop() 

    # handler for sending thread (call interval 0.05s -> 20Hz)
    def send(self):
        if  self.controlData is not None:
            self.usartConnection.send(self.controlData.data)
	    print "sending"
    
    # handler for receiving thread (call interval 0.05s -> 20Hz)   
    def receive(self):
        data = self.usartConnection.readData()
	dataLength = len(data)
        if dataLength == 0:
            self.timeoutCounter += 1
            if self.timeoutCounter >= self.maxTimeoutCounter:
                # TODO set controller state in latched DebugData as NO_CONNECTION
                print "USART receiving thread timeout ! - setting NO_CONNECTION"
                self.timeoutCounter = 0
            return
        self.timeoutCounter = 0

        i = 0
        while i < dataLength:  
            if self.proceedReceiving(data[i]):
                    # valid DebugData received
                    self.notifyIpConnection()
            i += 1

    preBuffer = ''
    dataBuffer = ''
    preambleFlag = False
    def proceedReceiving(self, ch):
        if ch == '$':
            self.preBuffer += ch
            if len(self.preBuffer) == 4:
                # preamble received, clear all
                self.preBuffer = ''
                self.dataBuffer = ''
                self.preambleFlag = True
            return False
        result = False
        if self.preambleFlag:
            if len(self.preBuffer) > 0:
                self.dataBuffer += self.preBuffer   
            if len(self.dataBuffer) < 34:
                self.dataBuffer += ch
            if len(self.dataBuffer) == 34:
                debug = DebugData("$$$$" + self.dataBuffer)
		print debug.toStringShort()
                if debug.isValid():
                    self.debugData = debug
                    result = True           
                self.preBuffer = ''
                self.dataBuffer = ''
                self.preambleFlag = False
        self.preBuffer = ''  
        return result
       
    def notifyIpConnection(self):
        if self.ipConnection is not None:
            self.ipConnection.setDebugData(self.debugData)
        else:
            print "Valid DebugData received but not forwarded - no IpConnection attached" 

    # latch newly received ControlData for sending thread
    def setControlData(self, message):
        msg = ControlData(message)
        if not msg.isValid():
          print "ERROR: wrong msg"
          return

        print time.strftime("%H:%M:%S"), msg.toStringShort()

        self.controlData = msg
