from DroneControler import DroneControler
from ControlData import *
from UartSender import *
from FakeUartSender import *
import time
from LogWriter import *
import struct

class IpConnectionMock:

    def setDebugData(self, debugData):
        pass

RB2 = "/dev/ttyAMA0"
RB3 = "/dev/ttyS0"

#TODO use settings here
#usart = FakeUartSender()
usart = UartSender(RB3, 115200)

logWriter = LogWriter()
droneControler = DroneControler(usart, logWriter)

# attach mock of handler for ip connection
ipConnectionMock = IpConnectionMock()
droneControler.setIpConnection(ipConnectionMock)

droneControler.enable()

droneControler.setControlData(ControlData.SomeValidControlCommand().data)

time.sleep(3)

droneControler.setControlData(ControlData.StopCommand().data)

time.sleep(0.05)

droneControler.disable()
droneControler.usartConnection.closeConnection()

print "DONE"
