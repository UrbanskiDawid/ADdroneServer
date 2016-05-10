import socket
from ControlData import *
from TimerThread import *
from StreamProcessor import *

adress = '52.58.5.47'
port = 6666


class IpClient:
    socket = None
    
    def __init__(self, adress, port):
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        try:
            s.connect((adress, port))
        except:
            print 'Unable to connect to the server!'
            sys.exit()

        print 'Successfuly connected to the server'

    
    def send(self, data):
        print 'Sending: ', data
        socket.send(data)

    def proceedReceiving(self):
        BUFFER_SIZE = 512
        try:
          data = self.connection.recv(BUFFER_SIZE)
        except:
          data = None
          print 'IpClient: forwardIncomingPacket: IP receive ERROR/TIMEOUT'

        if not data:
            print 'IpController: client disconnected:', self.client_address
            return False

        print 'IpClient: received: [' + str(data.encode("hex") + ']'))
        return True

    def close(self):
        socket.close()


class ADdroneClient:
    sock = None
    controlData = None

    receivingThread = None
    sendingThread = None

    def sendingHandler(self):
        if self.controlData is not None:
            self.sock.send(self.controlData.data)

    def receivingHandler(self):
        self.sock.proceedReceiving()

    def __init__(self, adress, port):
        self.sock = IpClient(adress, port)
        
        self.sendingThread = TimerThread(sendingHandler, 0.5)
        self.receivingThread = TimerThread(receivingHandler, 0.01) 

    def setControlData(self, controlData):
        self.controlData = controlData

    def close(self):
        self.sock.close()
        self.receivingThread.close()
        self.sendingThread.close()




client = ADdroneClient(adress, port)

client.setControlData(ControlData.SomeValidControlCommand())

time.sleep(30)

client.setControlData(ControlData.StopCommand())

time.sleep(0.5)

client.close()



