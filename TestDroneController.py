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

# time parameters of test
duration = 15.0 # [s]
sendingFreq = 2.0 # [Hz]

i = 0
while i < sendingFreq * duration:
    i += 1
    droneControler.sendCommData(ControlData.SomeValidControlCommand())
    time.sleep(1 / sendingFreq)
        
i = 0
while i < sendingFreq * 1:
    i += 1
    droneControler.sendCommData(ControlData.StopCommand())
    time.sleep(1 / sendingFreq)

droneControler.close()

print "DONE"
