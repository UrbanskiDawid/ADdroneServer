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
   
usart = FakeUartSender()
# usart = UartSender("/dev/ttyAMA0", 19200)

logWriter = LogWriter()
droneControler = DroneControler(usart, logWriter)

# attach mock of handler for ip connection
ipConnectionMock = IpConnectionMock()
droneControler.setIpConnection(ipConnectionMock)

droneControler.enable()

time.sleep(0.5)

droneControler.setControlData(ControlData.SomeValidControlCommand().data)

time.sleep(3)

droneControler.setControlData(ControlData.StopCommand().data)

time.sleep(0.1)

droneControler.disable()

print "DONE"
