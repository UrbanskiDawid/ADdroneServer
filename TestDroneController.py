from DroneControler import DroneController
from ControlData import *
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
maxTime = 30

i = 0
while i < maxTime*2:
    i += 1
    droneControler.sendCommData(ControlData.SomeValidControlCommand())
    time.sleep(0.5)
        
i = 0
while i < 2:
    i += 1
    droneControler.sendCommData(ControlData.StopCommand())
    time.sleep(0.5)

droneControler.close()

print "DONE"
