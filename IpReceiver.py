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

    def __init__(self, server_address, use_simulator, droneControler, retryNumBind, logWriter):
        self.logWriter = logWriter
        if use_simulator:
            self.sock = mockupSocket()
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
            time.sleep(5)
        self.sock.listen(1)
        self.droneControler = droneControler

    def acceptConnection(self):
        self.keepConnectionFlag = False
        self.connection, self.client_address = self.sock.accept()
        self.keepConnectionFlag = True
        print('client connected:', self.client_address)
        self.logWriter.noteEvent('Client connected: ' + \
                                 str(self.client_address))
        self.droneControler.enable()

    def send(self, data):
        try:
          self.connection.send(data+"\n")
          self.logWriter.noteEvent('Socket: Send: ' + str(data))
        except:
          pass

    def forwardIncomingPacket(self):
        BUFFER_SIZE = 512
        try:
          bytesData = self.connection.recv(BUFFER_SIZE)
          self.logWriter.noteEvent('Socket: Received: ' + str(bytesData))
        except:
          bytesData = None
          print('forwardIncomingPacket: IP receive ERROR/TIMEOUT')

        if not bytesData:
           print('client timeout:', self.client_address)
           return

        self.droneControler.setControlData(bytesData)

    def closeConnection(self):
        self.keepConnectionFlag = False
        self.sock.close()
        self.droneControler.disable()

    def keepConnection(self):
        return self.keepConnectionFlag
