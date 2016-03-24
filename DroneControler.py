from Message import *
from threading import Thread,Event, Lock
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
    __uartSender = None
    __logWriter = None
    __controlDataLock = None

    def __init__(self, uartSender, logWriter):
        self.uartSender = uartSender
        self.controlDataLock = threading.Lock  # must preceed control data, as used in get/set
        self.__controlData = ''
        self.sendingThread = TimerThread(self.send, 0.05)
        self.receivingThread = TimerThread(self.receive, 0.01)
        self.__logWriter = logWriter

    def enable(self):
        self.sendingThread.start()
        self.receivingThread.start()
        
    def disable(self):
        self.sendingThread.stop()
        self.receivingThread.stop()
        # required? how do you think?
        self.sendingThread.join()
        self.receivingThread.join()

    # handler for sending thread (call interval 0.05s -> 20Hz)
    def send(self):
        data = self.getControlData(True)
        if len(data) > 0:
            self.uartSender.send(data)

    # handler for receiving thread (call interval 0.01s -> 100Hz)   
    def receive(self):
        data = self.uartSender.recv()
        if data:
            self.logWriter.noteEvent('UART: Received: ' + str(data))
            print("Data received from drone: " + str(data).rstrip())
        else:
            print("ERROR: No data received from drone")

    # latch newly received ControlData for sending thread
    # @controlData.setter
    def setControlData(self, message):
        msg = Message(message)
        if not msg.isValid():
            print("ERROR: wrong msg")
            return

        print(time.strftime("%H:%M:%S") + str(msg) + "[" + msg.toStringHex() + "]")
        self.controlDataLock.aquire()
        self.__controlData = message
        self.controlDataLock.release()

    # @property
    def getControlData(self, resetData = False):
        self.controlDataLock.aquire()
        data = self.__controlData
        if resetData:
            data = ""
        self.controlDataLock.release()
        return data

# class DroneControler2:
#     uartSender = None
#     stopWatchDog = False
#     rcvWatchDogThread = None
#     logWriter = None
#
#     def __init__(self, uartSender, logWriter):
#         self.uartSender = uartSender
#         self.logWriter =logWriter
#
#     def __del__(self):
#         self.stopUartRcvWatchdog()
#
#     def newInstruction(self, bytesMessage):
#         '''
#         :param bytesMessage: byte-like
#         '''
#         msg = Message(bytesMessage)
#         if not msg.isValid():
#             print("ERROR: wrong msg")
#             return
#
#         print(time.strftime("%H:%M:%S") + str(msg) + "[" + msg.toStringHex() + "]")
#         self.uartSender.send(bytesMessage)
#         self.logWriter.noteEvent('UART: Send: ' + str(msg))
#         self.startUartRcvWatchdog()
#
#     def startUartRcvWatchdog(self):
#         if not self.rcvWatchDogThread:
#             self.stopWatchDog = False
#             self.rcvWatchDogThread = threading.Thread(target=self.uartRcvWatchdog)
#             self.rcvWatchDogThread.start()
#
#     def stopUartRcvWatchdog(self):
#         if self.rcvWatchDogThread and self.rcvWatchDogThread.is_alive():
#             self.stopWatchDog = True
#             self.rcvWatchDogThread.join()
#             self.stopWatchDog = False
#             self.rcvWatchDogThread = None
#
#     def uartRcvWatchdog(self):
#         print("uartRcvWatchdog started")
#         sleepTime = 1
#         while not self.stopWatchDog:
#             time.sleep(sleepTime)
#             data = self.uartSender.recv()
#             if data:
#                 self.logWriter.noteEvent('UART: Received: ' + str(data))
#                 print("Data received in 1 sec from drone: " + str(data).rstrip())
#             else:
#                 print("ERROR: No data received in " + str(sleepTime) +" sec from drone")
#         print("uartRcvWatchdog finished")