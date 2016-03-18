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

    def __init__(self, uartSender):
        self.uartSender = uartSender
        self.debugData = '';
        self.controlData = '';
        self.sendingThread = TimerThread(self.send, 0.05)
        self.receivingThread = TimerThread(self.receive, 0.01)

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
        self.uartSender.readANS()
        # TODO implement receiving DebugData when ready on controller
        # use uartSender object after refactoring it to handle bidirectional communication

    # latch newly received ControlData for sending thread
    def setControlData(self, message):
        msg=Message(message)
        if not msg.isValid():
          print "ERROR: wrong msg"
          return

        print time.strftime("%H:%M:%S"),str(msg),"["+msg.toStringHex()+"]"

        self.controlData = message
