from DroneControler import DroneControler
from ControlData import *
from UartSender import *
import time
import struct

class IpConnectionMock:

    def setDebugData(self, debugData):
        pass
   
usart = UartSender("/dev/ttyAMA0", 19200)
        
droneControler = DroneControler(usart)

# attach mock of handler for ip connection
ipConnectionMock = IpConnectionMock()
droneControler.setIpConnection(ipConnectionMock)

droneControler.enable()

time.sleep(0.5)

droneControler.setControlData(ControlData.SomeValidControlData().data)

time.sleep(3)

droneControler.setControlData(ControlData.StopCommand().data)

time.sleep(0.1)

droneControler.disable()

print "DONE"
