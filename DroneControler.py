from UartSender import *
from Message import *
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
    uartSender = None

    def __init__(self, uartSender, logWriter):
        self.uartSender = uartSender
        self.debugData = '';
        self.controlData = '';
        self.sendingThread = TimerThread(self.send, 0.05)
        self.receivingThread = TimerThread(self.receive, 0.05)
        self.logWriter = logWriter

    def enable(self):
        self.sendingThread.start()
        self.receivingThread.start()
        
    def disable(self):
        self.sendingThread.stop()
        self.receivingThread.stop() 

    # handler for sending thread (call interval 0.05s -> 20Hz)
    def send(self):
        if  len(self.controlData) > 0:
            self.uartSender.send(self.controlData)
    
    # handler for receiving thread (call interval 0.01s -> 100Hz)   
    def receive(self):
        data = self.uartSender.recv()
        if data:
            self.logWriter.noteEvent('DroneController: Received: ' + str(data))
            print time.strftime("%H:%M:%S"), 'DroneController: Received: ' + str(data).rstrip()
        else:
            print "DroneController: ERROR: No data received from drone"

    # latch newly received ControlData for sending thread
    def setControlData(self, message):
        msg=Message(message)
        if not msg.isValid():
          print "ERROR: wrong msg"
          return

        print time.strftime("%H:%M:%S"),'DroneController: Send data set to: ',str(msg),"["+msg.toStringHex()+"]"

        self.controlData = message
