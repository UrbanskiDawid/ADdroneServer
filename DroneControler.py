from ControlData import *
from DebugData import *
from threading import Thread, Event, Lock
import time
from TimerThread import *
from FakeUartController import *
from UartController import *
from StreamProcessor import *


# object used to handle UART part for communication with controller
class DroneController:
    uartController = None

    receivingThread = None

    logWriter = None

    noDebugReceivingCounter = 0 
    maxTimeoutCounter = 20 # 20 * 0.05 = 1s

    onReceiveEvent = None # Event to call when read data from USART

    streamProcessor = None

    def __init__(self,uartDev, usartBaundRate, logWriter):
        self.uartController = UartController(uartDev, usartBaundRate)

        self.logWriter = logWriter
        self.onReceiveEvent = self.defaultOnReceiveEvent

        self.streamProcessor = StreamProcessor(self.onReceiveControl, self.onReceiveSignal, self.onReceiveAutopilot)

        self.receivingThread = TimerThread('receivingThread',self.receiveThread, 0.05) # 20 Hz
        self.receivingThread.start()

    #onReceiveEvent - call this function when new CommData is received via UART
    def setOnReceiveEvent(self, onReceiveEvent):
      self.onReceiveEvent = onReceiveEvent

    def defaultOnReceiveEvent(self, commData):
      self.logWriter.noteEvent('DroneController: defaultOnReceiveEvent' + str(commData))
        
    def close(self):
      print('DroneControler: close')
      TimerThread.kill(self.receivingThread)
      self.uartController.close()
              
    # Thread
    # uartConnection
    # handler for receiving thread
    def receiveThread(self):
        data = self.uartController.recv()
        dataLength = len(data)
        if dataLength == 0:
            self.noDebugReceivingCounter += 1
            if self.noDebugReceivingCounter >= self.maxTimeoutCounter:
                # build ERROR_CONNECTION DebugData and call onReceiveEvent
                debugData = DebugData.SomeValidDebugMessage()
                debugData.setConnectionLost()
                self.logWriter.noteEvent('DroneController: Error! Receiving thread timeout.')
                self.onReceiveEvent(debugData)
                self.noDebugReceivingCounter = 0
            return
        self.noDebugReceivingCounter = 0
        
        log_msg = 'DroneController: received: [0x' + str(data.encode("hex")) + ']'
        self.logWriter.noteEvent(log_msg)

        # push data to stream processor - when data packet is be received onReceive event will be called
        self.streamProcessor.processStream(data)

    # event called by StreamProcessor - on control preamble
    def onReceiveControl(self, debugDataMsg):
        debugData = DebugData(debugDataMsg)
        if debugData.isValid():
            # forward data to DronController
            self.onReceiveEvent(debugData)
            log_msg = 'DroneController: DebugData received: [' + str(debugData) + ']'
        else:
            log_msg = 'DroneController: INVALID DebugData received: [' + debugDataMsg + ']'
        self.logWriter.noteEvent(log_msg)

    # event called by StreamProcessor - on signal preamble
    def onReceiveSignal(self, signalPongMsg):
        # this event should never be called on Uart communication side
        log_msg = 'DroneController: Unexpected event received [' + str(signalPongMsg.encode("hex")) + ']'
        self.logWriter.noteEvent(log_msg)

    # event called by StreamProcessor - on autopilota preamble
    def onReceiveAutopilot(self, autopilotDataMsg):
        autopilotData = AutopilotData(autopilotDataMsg)
        if autopilotData.isValid():
            # forward data to DroneController
            self.onReceiveEvent(autopilotData)
            log_msg = 'DroneController: AutopilotData received [0x' + str(autopilotDataMsg.encode("hex")) + ']'
        else:
            log_msg = 'DroneController: INVALID AutopilotData received [0x' + autopilotDataMsg + ']'
        self.logWriter.noteEvent(log_msg)
 
    # send CommData to drone
    def sendCommData(self, commData):
        log_msg = 'DroneController: Forwarding CommData: [0x' + commData.data.encode("hex") + ']'
        self.logWriter.noteEvent(log_msg)
        self.uartController.send(commData.data)

    def getDebugData(self):
        return self.debugData
