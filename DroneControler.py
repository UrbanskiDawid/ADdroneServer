from Message import *
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
    uartSender = None
    logWriter = None
    __controlDataLock = None
    __controlData = None
    __nbReads = 0

    def __init__(self, uartSender, logWriter):
        self.uartSender = uartSender
        self.__controlDataLock = Lock()  # must preceed __controlData, as used in get/set
        self.__controlData = ''
        self.__nbReads = 0
        self.sendingThread = TimerThread(self.send, 0.05)        # 20 Hz
        self.receivingThread = TimerThread(self.receive, 0.025)  # 40 Hz
        self.logWriter = logWriter

    def enable(self):
        self.sendingThread.start()
        self.receivingThread.start()
        
    def disable(self):
        self.sendingThread.stop()
        self.receivingThread.stop() 

    # handler for sending thread
    def send(self):
        data = self.getControlData()
        if len(data) > 0:
            self.uartSender.send(data)

            self.logWriter.noteEvent('DroneController: Send: [' + data + ']')
            print time.strftime("%H:%M:%S ") + 'DroneController: Send: [' + data + ']'

    # handler for receiving thread
    def receive(self):
        data = self.uartSender.recv()
        if data:

            self.logWriter.noteEvent('DroneController: Received: [' + str(data) + ']')
            print time.strftime("%H:%M:%S ") + 'DroneController: Received: [' + str(data) + ']'
        else:
            print "DroneController: WARNING: No data received from drone"

    def setControlData(self, value):
        msg = Message(value)
        if not msg.isValid():
            print time.strftime("%H:%M:%S ") + "DroneController: ERROR: wrong msg"
            return

        print time.strftime("%H:%M:%S ") + 'DroneController: Send data set to: ' + str(msg) + "["+msg.toStringHex()+"]"

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
