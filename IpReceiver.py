import socket
import sys
import time
from mockupSocket import *

class IpReceiver:
    sock = None
    connection = None
    droneControler = None
    keepConnectionFlag = False
    client_address = None
    logWriter = None

    def __init__(self, server_address, use_simulator, simulatorLoopData, droneControler, retryNumBind, logWriter):
        self.logWriter = logWriter
        if use_simulator:
            self.sock = mockupSocket(simulatorLoopData)
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tryNum=retryNumBind
        while True:
          try:
            self.sock.bind(server_address)
            break
          except Exception as e:
            sys.stderr.write('IpReceiver: failed ({0}/{1}): {2}\n'.format(tryNum,retryNumBind,e))
            tryNum-=1
            if tryNum<1:
              raise Exception("IpReceiver can't bind socket!")
              #end of execution - exception raised
            time.sleep(5)
        self.sock.listen(1)
        self.droneControler = droneControler

    def acceptConnection(self):
        self.keepConnectionFlag = False
        self.connection, self.client_address = self.sock.accept()
        self.keepConnectionFlag = True
        print 'client connected:', self.client_address
        self.logWriter.noteEvent('Client connected: ' + \
                                 str(self.client_address))
        self.droneControler.enable()

    def send(self, data):
        try:
          self.connection.send(data+"\n")
          self.logWriter.noteEvent('Socket: Send: ' + str(data))
        except:
          pass

    msg=''
    def forwardIncomingPacket(self):
        BUFFER_SIZE = 512
        try:
          data = self.connection.recv(BUFFER_SIZE)
          self.logWriter.noteEvent('Received: ' + str(data))
        except:
          data = None
          print 'forwardIncomingPacket: IP receive ERROR/TIMEOUT'

        if not data:
            print 'client disconnected:', self.client_address
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
              self.droneControler.setControlData(self.msg)
              self.msg=[]

    def setDebugData(self, debugData):
        pass
        #msgToSendViaIp = debugData.msg
        # TODO implement sending DebugData via IP connection

    def closeConnection(self):
        self.keepConnectionFlag = False
        self.sock.close()
        self.droneControler.disable()

    def keepConnection(self):
        return self.keepConnectionFlag
