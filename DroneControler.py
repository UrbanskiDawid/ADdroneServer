from ControlData import *
from DebugData import *
from threading import Thread, Event, Lock
import time
from TimerThread import *
from FakeUartController import *
from     UartController import *


#this is DroneControler
# is is used to handle USART part
class DroneController:
    __uartController = None
    __controlDataLock = None    
    __controlData = None
    __debugData = None #NOT IN USE?!
    __sendingThread = None
    __receivingThread = None
    __logWriter = None
    __nbReads = 0
    __maxTimeoutCounter = 20 # 20 * 0.05 = 1s
    __timeoutCounter = 0
    __preBuffer = ''
    __dataBuffer = ''
    __preambleFlag = False
    __onReceive = None #Event to call when read data from USART

    #onReceiveEvent - call this function when new message is recived
    #uartDev - None if usartFake=true
    #usartBaundRate - None if usartFake=true
    #usartFake - True -> UartController else FakeUartController
    def __init__(self,onReceiveEvent, uartDev, usartBaundRate, usartFake, logWriter):

        if usartFake == True:
            self.__uartController = FakeUartController()
        else:
            self.__uartController = UartController(usartDev, usartBaundRate)

        self.__controlDataLock = Lock()
        self.__logWriter = logWriter
        self.__onReceive = onReceiveEvent

        self.__sendingThread = TimerThread("sendingThread",self.__sendThread, 0.05)        # 20 Hz
        self.__sendingThread.start()

        self.__receivingThread = TimerThread("receivingThread",self.__receiveThread, 0.05)   # 20 Hz
        self.__receivingThread.start()
        
    def close(self):
      print('DroneControler: close');
      TimerThread.kill(self.__sendingThread)
      TimerThread.kill(self.__receivingThread)
      self.__uartController.close()

    # Thread
    # usartConnection
    # handler for sending thread
    def __sendThread(self):
        data = self.getControlData()
        if data is not None:
            self.__uartController.send(data)
            log_msg = 'DroneController: Send: [' + data.encode("hex") + ']'
            self.__logWriter.noteEvent(log_msg)
            #print time.strftime("%H:%M:%S ") + log_msg
    
    # Thread
    # usartConnection
    # handler for receiving thread
    def __receiveThread(self):
        data = self.__uartController.recv()
        dataLength = len(data)
        if dataLength == 0:
            self.__timeoutCounter += 1
            if self.__timeoutCounter >= self.__maxTimeoutCounter:
                # TODO set controller state in latched __debugData as NO_CONNECTION
                print "USART receiving thread timeout ! - setting NO_CONNECTION"
                self.__timeoutCounter = 0
            else:
                print "DroneController: WARNING: No data received from drone [" + str(self.__timeoutCounter) + "] time(s)"
            return
        self.__timeoutCounter = 0

        log_msg = 'DroneController: received: [0x' + data.encode("hex") + ']'
        self.__logWriter.noteEvent(log_msg)
#        print time.strftime("%H:%M:%S ") + log_msg

        i = 0
        while i < dataLength:  
            if self.__proceedReceiving(data[i]):
              self.__onReceive(self.__debugData)
                    # valid DebugData received
#                    self.notifyIpConnection()
            # TODO difficult to detect wrong data. Impossible to print or log error message
            i += 1

    #part of __receiveThread
    def __proceedReceiving(self, ch):
        if ch == '$':
            self.__preBuffer += ch
            if len(self.__preBuffer) == 4:
                # preamble received, clear all
                self.__preBuffer = ''
                self.__dataBuffer = ''
                self.__preambleFlag = True
            return False
        result = False
        if self.__preambleFlag:
            if len(self.__preBuffer) > 0:
                self.__dataBuffer += self.__preBuffer   
            if len(self.__dataBuffer) < 34:
                self.__dataBuffer += ch
            if len(self.__dataBuffer) == 34:
                debug = DebugData("$$$$" + self.__dataBuffer)
                if debug.isValid():
                    self.__debugData = debug
                    result = True
                    log_msg = 'DroneController: valid DebugDataReceived: [' + str(debug) + ']'
                else:
                    log_msg = 'DroneController: INVALID DebugDataReceived: [' + str(debug) + ']'

                self.__logWriter.noteEvent(log_msg)
#                print time.strftime("%H:%M:%S ") + log_msg

                self.__preBuffer = ''
                self.__dataBuffer = ''
                self.__preambleFlag = False

        self.__preBuffer = ''  
        return result
 
    # latch newly received ControlData for sending thread
    def setControlData(self, value):
        controlData = ControlData(value)
        if not controlData.isValid():
            print time.strftime("%H:%M:%S ") + "DroneController: ERROR: wrong ControlData"
            return

        log_message = 'DroneController: Send data set to: ' + str(controlData) + "[" + controlData.toStringHex() + "]"
        self.__logWriter.noteEvent(log_message)

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
#            print time.strftime("%H:%M:%S") + " " + log_message
            self.__logWriter.noteEvent(log_message)
        return data

