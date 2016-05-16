import socket
import sys
import time
from ControlData import *
from mockupSocket import *
from TimerThread import *
from StreamProcessor import *

class IpController:
    sock = None
    connection = None
    keepConnectionFlag = False
    client_address = None
    logWriter = None
    onReciceEvent = None #function one argument

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

        self.streamProcessor = StreamProcessor(self.onReceiveControl, self.onReceiveSignal)

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

    def setOnReceiveEvent(self,reciveEvent):
        self.onReciceEvent=reciveEvent

    def defaultOnReciveEvent(self,dd):#DebugData
        self.logWriter.noteEvent('IpController: defaultOnReciveEvent "'+str(dd)+'"');

    def acceptConnection(self):
        self.keepConnectionFlag = False
        self.connection, self.client_address = self.sock.accept()
        self.keepConnectionFlag = True
        print 'IpController: client connected:', self.client_address
        self.logWriter.noteEvent('IpController: Client connected: ' + \
                                 str(self.client_address))

    def icConnected(self):
        return not (self.connection==None)

    def send(self, data):
        if not self.icConnected():
          return False
        try:
          self.connection.send(data)
          log_msg='IpController: send: [0x'+str(data.encode("hex"))+'] len:'+str(len(data))
        except Exception as e:
          log_msg='IpController: send failed: '+str(data)+" Exception: "+str(e)
        #print log_msg
        self.logWriter.noteEvent(log_msg)

    def forwardIncomingPacket(self):
      return self.forwardIncomingPacket2()

    msg=''
    def forwardIncomingPacket1(self):
        BUFFER_SIZE = 512
        try:
          data = self.connection.recv(BUFFER_SIZE)
          self.logWriter.noteEvent('IpController: received: [0x' + str(data.encode("hex")+']'))
        except:
          data = None
          print 'IpController: forwardIncomingPacket: IP receive ERROR/TIMEOUT'

        if not data:
            print 'IpController: client disconnected:', self.client_address
            self.keepConnectionFlag = False
            return

        i=0
        dLen=len(data)
        while i<dLen:
          if len(self.msg)==0:#no msg
            if i+4>dLen:
              break
            if data[i+0]=='$' and data[i+1]=='$' and data[i+2]=='$' and data[i+3]=='$':
              self.msg='$$$$'
              i+=4
              continue
            i+=4
          else:
            self.msg+=str(data[i])
            i+=1
            if len(self.msg) == 38:
              newControlData = ControlData(self.msg)
              if newControlData.isValid():
                log_msg = 'IpController: ControlData received: [' + str(newControlData) + ']'
                self.onReciceEvent(newControlData)#self.msg)
              else:
                log_msg = 'IpController: INVALID ControlData received: [' + str(self.msg) + ']'
              self.logWriter.noteEvent(log_msg)
              self.msg=[]

    # event called by StreamProcessor - on control preamble
    def onReceiveControl(self, controlDataMsg):
        newControlData = ControlData(controlDataMsg)
        if newControlData.isValid():
            # forward data to DronController
            self.onReciceEvent(newControlData)
            log_msg = 'IpController: received ControlData: [' + str(newControlData) + ']'
        else:
            log_msg = 'IpController: received INVALID ControlData: [' + str(self.msg) + ']'
        self.logWriter.noteEvent(log_msg)

    # event called by StreamProcessor - on signal preamble
    def onReceiveSignal(self, signalPongMsg):
        # immadetely response with ping
        self.send(signalPongMsg)
        log_msg = 'IpController: Signal received [0x' + str(signalPongMsg.encode("hex")) + '] len:'+str(len(signalPongMsg))
        self.logWriter.noteEvent(log_msg)

    def forwardIncomingPacket2(self):
        BUFFER_SIZE = 512
        try:
          data = self.connection.recv(BUFFER_SIZE)
          log_msg='IpController: received: [0x' + str(data.encode("hex"))+']'
#          print log_msg
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
