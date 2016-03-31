from DroneControler import DroneControler
from ControlData import *
from UartSender import *
import time
import struct

class IpConnectionMock:

    def setDebugData(self, debugData):
        pass
   
usart = UartSender("/dev/ttyAMA0", 115200)
        
droneControler = DroneControler(usart)

# attach mock of handler for ip connection
ipConnectionMock = IpConnectionMock()
droneControler.setIpConnection(ipConnectionMock)

droneControler.enable()

droneControler.setControlData(ControlData.SomeValidControlData().data)

time.sleep(3)

droneControler.setControlData(ControlData.StopCommand().data)

time.sleep(0.05)

droneControler.disable()

print "DONE"
