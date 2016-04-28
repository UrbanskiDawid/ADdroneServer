from ControlData import *
from DebugData import *
from threading import Thread, Event, Lock
import time
from TimerThread import *
from FakeUartController import *
from     UartController import *


# object used to handle UART part for communication with controller
class DroneController:
    uartController = None

    controlDataLock = None    
    controlData = None
    debugData = None

    sendingThread = None
    receivingThread = None

    logWriter = None

    nbReads = 0
    maxTimeoutCounter = 20 # 20 * 0.05 = 1s
    timeoutCounter = 0

    preBuffer = ''
    dataBuffer = ''
    preambleFlag = False

    onReceive = None # Event to call when read data from USART

    #uartDev - None if usartFake=true
    #usartBaundRate - None if usartFake=true
    #usartFake - True -> UartController else FakeUartController
    def __init__(self,uartDev, usartBaundRate, usartFake, logWriter):

        if usartFake == True:
            self.uartController = FakeUartController()
        else:
            self.uartController = UartController(uartDev, usartBaundRate)

        self.controlDataLock = Lock()
        self.logWriter = logWriter
        self.onReceive = self.defaultOnReceiveEvent

        self.sendingThread = TimerThread('sendingThread',self.sendThread, 0.05) # 20 Hz
        self.sendingThread.start()

        self.receivingThread = TimerThread('receivingThread',self.receiveThread, 0.05) # 20 Hz
        self.receivingThread.start()

    #onReceiveEvent - call this function when new DebugData is recived via UART
    def setOnReceiveEvent(self, onReceiveEvent):
      self.onReceive = onReceiveEvent

    def defaultOnReceiveEvent(self, debugData):
      self.logWriter.noteEvent('DroneController: defaultOnReceiveEvent')
        
    def close(self):
      print('DroneControler: close');
      TimerThread.kill(self.sendingThread)
      TimerThread.kill(self.receivingThread)
      self.uartController.close()

    # Thread
    # uartConnection
    # handler for sending thread
    def sendThread(self):
        data = self.getControlData()
        if data is not None:
            log_msg = 'DroneController: Send ControlData: [0x' + data.data.encode("hex") + ']'
            self.logWriter.noteEvent(log_msg)
            self.uartController.send(data)
            print 'Send: ' + str(data)
                
    # Thread
    # uartConnection
    # handler for receiving thread
    def receiveThread(self):
        data = self.uartController.recv()
        dataLength = len(data)
        if dataLength == 0:
            self.timeoutCounter += 1
            if self.timeoutCounter >= self.maxTimeoutCounter:
                # TODO set controller state in latched debugData as NO_CONNECTION
                # TODO call onReceiveEvent for transmi error via IP
                print 'DroneController: receiving thread timeout !'
                self.timeoutCounter = 0
            return
        self.timeoutCounter = 0

        i = 0
        while i < dataLength:  
            if self.proceedReceiving(data[i]):
                log_msg = 'DroneController: Received DebugData: [0x' + self.debugData.data.encode("hex") + ']'
                self.logWriter.noteEvent(log_msg)
                self.onReceive(self.debugData)
                print 'Received: ' + str(self.debugData)
            i += 1

    # proceed one char received via UART
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
                    self.debugData = debug
                    result = True

                self.preBuffer = ''
                self.dataBuffer = ''
                self.preambleFlag = False

        self.preBuffer = ''  
        return result
 
    # latch newly received ControlData for sending thread
    def setControlData(self, controlData):
        if not controlData.isValid():
            log_message = 'DroneController: ERROR: wrong ControlData set'
            self.logWriter.noteEvent(log_message)
            print log_message
            return

        log_message = 'DroneController: ControlData set to: [' + str(controlData) + ']'
        self.logWriter.noteEvent(log_message)

        self.controlDataLock.acquire()
        self.controlData = controlData
        self.nbReads = 0
        self.controlDataLock.release()

    def getControlData(self):
        self.controlDataLock.acquire()
        data = self.controlData
        self.nbReads += 1
        nbReads = self.nbReads
        self.controlDataLock.release()
        if nbReads > 1:
            log_message = 'DroneController: WARNING same ControlData read [' + str(nbReads) + '] times.'
            self.logWriter.noteEvent(log_message)
        return data

    def getDebugData(self):
        return self.debugData
