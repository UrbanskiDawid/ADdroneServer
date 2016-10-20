import socket
import sys
import time
from TimerThread import *

class AdapterServer:
    sock = None
    connection = None
    keepConnectionFlag = False
    client_address = None

    onReceiveEvent = None  # function one argument

    def __init__(self, server_address, retryNumBind):
        self.onReceiveEvent = self.defaultOnReceiveEvent

        tryNum = retryNumBind
        while True:
            try:
                self.sock.bind(server_address)
                break
            except Exception as e:
                sys.stderr.write('IpController: failed ({0}/{1}): {2}\n'.format(tryNum, retryNumBind, e))
                tryNum -= 1
                if tryNum < 1:
                    raise Exception("IpController: can't bind socket!")
                    # end of method execution - exception raised
                time.sleep(5)
        self.sock.listen(1)


    def setOnReceiveEvent(self, receiveEvent):
        self.onReceiveEvent = receiveEvent


    def defaultOnReceiveEvent(self, data):
        print "AdapterServer: default on receive event"

    def acceptConnection(self):
        self.keepConnectionFlag = False
        self.connection, self.client_address = self.sock.accept()
        self.keepConnectionFlag = True
        print "AdapterServer: client connected:', self.client_address"

    def icConnected(self):
        return not (self.connection is None)

    def sendData(self, data):
        if not self.icConnected():
            return False
        try:
            self.connection.send(data)
        except Exception as e:
            print "IpController: send failed: " + str(e)

    def forwardData(self, usart):
        BUFFER_SIZE = 512
        try:
            data = self.connection.recv(BUFFER_SIZE)

        except:
            data = None
            print 'IpController: forwardIncomingPacket: IP receive ERROR/TIMEOUT'

        if not data:
            print 'IpController: client disconnected:', self.client_address
            self.keepConnectionFlag = False
            return

        usart.send(data)

    def close(self):
        self.keepConnectionFlag = False
        self.sock.close()

# server for IP connection
adapterServer = AdapterServer((server_name, SETTINGS.PORT), 5)

# USART controller for board connection
usartController = UartController("/dev/ttyAMA0", 115200)

def usartReceivingThreadHandle():
    global usartController
    global adapterServer
    data = usartController.recv()
    dataLength = len(data)
    if dataLength != 0:
        adapterServer.sendData(data)

receivingThread = TimerThread('receivingThread', receiveThread, 0.02) # 50 Hz


print('MainThread: waiting for a connection')
adapterServer.acceptConnection()
receivingThread.start()
while adapterServer.keepConnection():
    adapterServer.forwardData(usartController)
print('MainThread: connection closed')
print "Cosing interfaces..."

receivingThread.stop()

adapterServer.close()
usartController.close()

print "Done!"



