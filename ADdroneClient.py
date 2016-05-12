import socket
from ControlData import *
from TimerThread import *
from StreamProcessor import *

adress = '52.58.5.47'
port = 6666


class ADdroneClient:
    sock = None
    streamProcessor = None

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
            self.sock.send('%%%%abcd')
            
            

    """ on receive handlers """
    def onDebugReceive(self, data):
        print onDebugReceive
        pass

    def onPongReceive(self, data):
        isPongReceived = True
        now = datetime.datetime.now()
        print 'onPongReceive: ' + (d.seconds*1000 + d.microseconds/1000)
        pass


    def __init__(self, adress, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        try:
            s.connect((adress, port))
        except:
            print 'Unable to connect to the server!'
            sys.exit()

        print 'Successfuly connected to the server'       

        self.streamProcessor = StreamProcessor(self.onDebugReceive, self.onPongReceive)

        self.sendingControlThread = TimerThread(self.sendingControlHandler, 0.1)
        self.sendingSignalThread = TimerThread(self.sendingSignalHandler, 1.0)


    def receivingHandler(self):
        self.sock.proceedReceiving()
        
    def setControlData(self, controlData):
        self.controlData = controlData

    def close(self):
        self.sock.close()
        self.sendingControlThread.close()
        self.sendingSignalThread.close()




client = ADdroneClient(adress, port)

client.setControlData(ControlData.SomeValidControlCommand())

time.sleep(30)

client.setControlData(ControlData.StopCommand())

time.sleep(0.5)

client.close()



