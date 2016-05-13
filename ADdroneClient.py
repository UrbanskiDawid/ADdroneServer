import socket
from ControlData import *
from TimerThread import *
from StreamProcessor import *

adress = '52.58.5.47'
port = 6666

connectionTime = 30 # seconds


class ADdroneClient:
    sock = None
    streamProcessor = None
    keepConnectionFlag = False

    """ ControlData sending """
    controlData = None
    sendingControlThread = None

    # method called by sending thread to send ControlData to server
    def sendingControlHandler(self):
        if self.controlData is not None:
            self.sock.send(self.controlData.data)

    """ Ping sending """
    pingTimestamp = None
    pingData = None
    isPongReceived = True
    sendingSignalThread = None

    # method called by sending thread to send Ping to server
    # sending is only avalible when previous Pong was received
    def sendingSignalHandler(self):
        if isPongReceived:
            pingData = '%%%%abcd'
            isPongReceived = False
            pingTimestamp = datetime.datetime.now()
            self.sock.send(pingData)
            
            

    """ on receive handlers """
    def onDebugReceive(self, data):
        print onDebugReceive
        pass

    def onPongReceive(self, data):
        if data == pingData:
            now = datetime.datetime.now()
            isPongReceived = True
            d = now - pingTimestamp
            print 'onPongReceive: ' + (d.seconds*1000 + d.microseconds/1000)
        else:
            print 'Bad data received at signal chanell'


    def __init__(self, adress, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        try:
            s.connect((adress, port))
        except:
            print 'Unable to connect to the server!', adress, ':', port
            sys.exit()

        print 'Successfuly connected to the server', adress, ':', port      

        self.keepConnectionFlag = True

        self.streamProcessor = StreamProcessor(self.onDebugReceive, self.onPongReceive)

        self.sendingControlThread = TimerThread(self.sendingControlHandler, 0.1)
        self.sendingSignalThread = TimerThread(self.sendingSignalHandler, 1.0)


    def proceedReceiving(self):
        BUFFER_SIZE = 512
        try:
          data = self.connection.recv(BUFFER_SIZE)
        except:
          data = None
          print 'proceedReceiving: IP receive ERROR/TIMEOUT'

        if not data:
            print 'IpController: client disconnected:', self.client_address
            self.keepConnectionFlag = False
            return

        self.streamProcessor.processStream(data)
        
    def setControlData(self, controlData):
        self.controlData = controlData

    def close(self):
        self.sock.close()
        self.sendingControlThread.close()
        self.sendingSignalThread.close()




client = ADdroneClient(adress, port)

client.setControlData(ControlData.SomeValidControlCommand())

startTime = datetime.datetime.now()

exitingFlag = False
exitTime = None

while client.keepConnectionFlag:
    client.proceedReceiving()
    deltaTime = datetime.datetime.now() - startTime
    if deltaTime.second > connectionTime:
        # start disconection procedure
        if not exitingFlag:
            exitTime = datetime.datetime.now()
        client.setControlData(ControlData.StopCommand()) 
        exitingFlag = True
        deltaExitingTime = datetime.datetime.now() - startTime 
        if deltaExitingTime.second > 1:
            client.keepConnectionFlag = False

print 'Closing connection after ', connectionTime, ' seconds'

client.close()

print 'DONE'



