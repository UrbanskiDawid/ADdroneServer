import socket
import sys
import time
from ControlData import *
from AutopilotData import *
from mockupSocket import *
from TimerThread import *
from StreamProcessor import *

class IpController:
    sock = None
    connection = None
    keepConnectionFlag = False
    client_address = None
    logWriter = None
    
    onReceiveEvent = None #function one argument

    streamProcessor = None

    def __init__(self, server_address, use_simulator, simulatorLoopData, retryNumBind, logWriter):
        self.onReciceEvent=self.defaultOnReciveEvent
        self.logWriter = logWriter
        if use_simulator:
            self.sock = mockupSocket(simulatorLoopData)
            print('IpController: using port simulator')
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('IpController: Using ' + str(server_address[1]))

        self.streamProcessor = StreamProcessor(self.onReceiveControl, self.onReceiveSignal, self.onReceiveAutopilot)

        tryNum=retryNumBind
        while True:
          try:
            self.sock.bind(server_address)
            break
          except Exception as e:
            sys.stderr.write('IpController: failed ({0}/{1}): {2}\n'.format(tryNum,retryNumBind,e))
            tryNum-=1
            if tryNum<1:
              raise Exception("IpController: can't bind socket!")
              #end of method execution - exception raised
            time.sleep(5)
        self.sock.listen(1)

    def setOnReceiveEvent(self, receiveEvent):
        self.onReceiveEvent = receiveEvent

    def defaultOnReciveEvent(self, commData):
        self.logWriter.noteEvent('IpController: defaultOnReceiveEvent, data: ' + str(commData))

    def acceptConnection(self):
        self.keepConnectionFlag = False
        self.connection, self.client_address = self.sock.accept()
        self.keepConnectionFlag = True
        print 'IpController: client connected:', self.client_address
        self.logWriter.noteEvent('IpController: Client connected: ' + \
                                 str(self.client_address))

    def icConnected(self):
        return not (self.connection is None)

    def sendCommData(self, data):
        if not self.icConnected():
          return False
        try:
          self.connection.send(data)
          log_msg = 'IpController: send: [0x' + str(data.encode("hex")) + '] len:' + str(len(data))
        except Exception as e:
          log_msg = 'IpController: send failed: ' + str(data) + " Exception: " + str(e)
        
        self.logWriter.noteEvent(log_msg)

    # event called by StreamProcessor - on control preamble
    def onReceiveControl(self, controlDataMsg):
        controlData = ControlData(controlDataMsg)
        if controlData.isValid():
            # forward data to DronController
            self.onReceiveEvent(controlData)
            log_msg = 'IpController: ControlData received: [' + str(controlData) + ']'
        else:
            log_msg = 'IpController: INVALID ControlData received: [' + controlDataMsg + ']'
        self.logWriter.noteEvent(log_msg)

    # event called by StreamProcessor - on signal preamble
    def onReceiveSignal(self, signalPongMsg):
        # immadetely response with ping
        self.sendCommData(signalPongMsg)
        log_msg = 'IpController: Signal received [0x' + str(signalPongMsg.encode("hex")) + ']'
        self.logWriter.noteEvent(log_msg)

    # event called by StreamProcessor - on autopilot preamble
    def onReceiveAutopilot(self, autopilotDataMsg):
        autopilotData = AutopilotData(autopilotDataMsg)
        if autopilotData.isValid():
            # forward data to DroneController
            self.onReceiveEvent(autopilotData)
            log_msg = 'IpController: AutopilotData received [0x' + str(autopilotDataMsg.encode("hex")) + ']'
        else:
            log_msg = 'IpController: INVALID AutopilotData received [0x' + autopilotDataMsg + ']'
        self.logWriter.noteEvent(log_msg)
   

    def forwardIncomingPacket(self):
        BUFFER_SIZE = 512
        try:
          data = self.connection.recv(BUFFER_SIZE)
          log_msg='IpController: received: [0x' + str(data.encode("hex"))+']'
          self.logWriter.noteEvent(log_msg)
          
        except:
          data = None
          print 'IpController: forwardIncomingPacket: IP receive ERROR/TIMEOUT'

        if not data:
            print 'IpController: client disconnected:', self.client_address
            self.keepConnectionFlag = False
            return

        self.streamProcessor.processStream(data)

    def close(self):
        self.keepConnectionFlag = False
        self.sock.close()

    def keepConnection(self):
        return self.keepConnectionFlag
