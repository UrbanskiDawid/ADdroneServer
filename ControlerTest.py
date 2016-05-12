from DroneControler import DroneController
from ControlData import *
from UartSender import *
import time
from LogWriter import *
import struct

RB2 = "/dev/ttyAMA0"
RB3 = "/dev/ttyS0"

def onReceiveUsart(debugData):
    pass


logWriter = LogWriter()
droneControler = DroneController(RB2, 115200, False, logWriter)

droneControler.setOnReceiveEvent(onReceiveUsart)

droneControler.setControlData(ControlData.SomeValidControlCommand())

time.sleep(60)

droneControler.setControlData(ControlData.StopCommand())

time.sleep(0.5)

droneControler.close()

print "DONE"
