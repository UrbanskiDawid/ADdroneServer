from DroneControler import DroneController
from ControlData import *
from UartSender import *
import time
from LogWriter import *
import struct

RB2 = "/dev/ttyAMA0"
RB3 = "/dev/ttyS0"

def onReceiveUsart(debugData):
    print debugData.toStringShort()


logWriter = LogWriter()
droneControler = DroneController(RB2, 115200, False, logWriter)

droneControler.setOnReceiveEvent(onReceiveUsart)

droneControler.setControlData(ControlData.SomeValidControlCommand().data)

time.sleep(10)

droneControler.setControlData(ControlData.StopCommand().data)

time.sleep(0.05)

droneControler.close()

print "DONE"
