from DroneControler import DroneController
from ControlData import *
from UartSender import *
import time
from LogWriter import *
import struct

RB2 = "/dev/ttyAMA0"
RB3 = "/dev/ttyS0"

def onReceiveUsart(debugData):
    print 'Recived:', str(debugData)


logWriter = LogWriter('logs')
droneControler = DroneController(RB2, 115200, False, logWriter)

droneControler.setOnReceiveEvent(onReceiveUsart)

# time of test in seconds
maxTime = 10

i = 0
while i < maxTime*10:
    i += 1
    droneControler.setControlData(ControlData.SomeValidControlCommand())
    time.sleep(0.1)

i = 0
while i < 5:
    i += 1
    droneControler.setControlData(ControlData.StopCommand())
    time.sleep(0.1)

droneControler.close()

print "DONE"
