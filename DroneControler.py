from ControlData import *
from threading import Thread, Event, Lock
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
# TODO make all members private
    usartConnection = None
    ipConnection = None
    __controlDataLock = None    
    __controlData = None
    __debugData = None
    sendingThread = None
    receivingThread = None
    logWriter = None
    __nbReads = 0
    maxTimeoutCounter = 20 # 20 * 0.05 = 1s
    timeoutCounter = 0
    preBuffer = ''
    dataBuffer = ''
    preambleFlag = False

    def __init__(self, usartConnection, logWriter):
        self.usartConnection = usartConnection
        self.__controlDataLock = Lock()
        self.logWriter = logWriter

    def setIpConnection(self, ipConnection):
        self.ipConnection = ipConnection

    def enable(self):
        if self.sendingThread is None and self.receivingThread is None:
            self.sendingThread = TimerThread(self.send, 0.05)        # 20 Hz
            self.receivingThread = TimerThread(self.receive, 0.05)   # 20 Hz
            self.sendingThread.start()
            self.receivingThread.start()
        else:
            print "ERROR: UART threads are allready not none"
        
    def disable(self):
        self.sendingThread.stop()
        self.receivingThread.stop()
        self.sendingThread.join()
        self.receivingThread.join()
        self.sendingThread = None
        self.receivingThread = None

    # handler for sending thread
    def send(self):
        data = self.getControlData()
        if data is not None:
            self.usartConnection.send(data)
            self.logWriter.noteEvent('DroneController: Send: [' + data + ']')
            print time.strftime("%H:%M:%S ") + 'DroneController: Send: [' + data + ']'
    
    # handler for receiving thread
    def receive(self):
        data = self.usartConnection.recv()
        dataLength = len(data)
        if dataLength == 0:
            self.timeoutCounter += 1
            if self.timeoutCounter >= self.maxTimeoutCounter:
                # TODO set controller state in latched __debugData as NO_CONNECTION
                print "USART receiving thread timeout ! - setting NO_CONNECTION"
                self.timeoutCounter = 0
            else:
                print "DroneController: WARNING: No data received from drone [" + str(self.timeoutCounter) + "] time(s)"
            return
        self.timeoutCounter = 0

        self.logWriter.noteEvent('DroneController: Received: [' + str(data) + ']')
        print time.strftime("%H:%M:%S ") + 'DroneController: Received: [' + str(data) + ']'

        i = 0
        while i < dataLength:  
            if self.proceedReceiving(data[i]):
                    # valid DebugData received
                    self.notifyIpConnection()
            # TODO difficult to detect wrong data. Impossible to print or log error message
            i += 1

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
                if debug.isValid():
                    self.__debugData = debug
                    result = True
                    log_msg = 'DroneController: valid DebugDataReceived: [' + str(data) + ']'
                else:
                    log_msg = 'DroneController: INVALID DebugDataReceived: [' + str(data) + ']'

                self.logWriter.noteEvent(log_msg)
                print time.strftime("%H:%M:%S ") + log_msg

                self.preBuffer = ''
                self.dataBuffer = ''
                self.preambleFlag = False

        self.preBuffer = ''  
        return result
       
    def notifyIpConnection(self):
        if self.ipConnection is not None:
            self.ipConnection.setDebugData(self.__debugData)
        else:
            print "Valid DebugData received but not forwarded - no IpConnection attached" 

    # latch newly received ControlData for sending thread
    def setControlData(self, value):
        controlData = ControlData(value)
        if not controlData.isValid():
            print time.strftime("%H:%M:%S ") + "DroneController: ERROR: wrong ControlData"
            return

        print time.strftime("%H:%M:%S ") + 'DroneController: Send data set to: ' + str(controlData) + "[" + controlData.toStringHex() + "]"

        self.__controlDataLock.acquire()
        self.__controlData = value
        self.__nbReads = 0
        self.__controlDataLock.release()

    def getControlData(self):
        self.__controlDataLock.acquire()
        data = self.__controlData
        self.__nbReads += 1
        nbReads = self.__nbReads
        self.__controlDataLock.release()
        if nbReads > 1:
            log_message = 'DroneController: Waring: same data read [' + str(nbReads) + '] times.'
            print time.strftime("%H:%M:%S") + " " + log_message
            self.logWriter.noteEvent(log_message)
        return data

