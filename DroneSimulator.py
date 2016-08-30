from ControlData import *
from DebugData import *
from TimerThread import *
from DebugDataValue import *
import math
import time
import random

class DroneSimulator:
    simulatorThread = None

    logWriter = None

    onReceiveEvent = None # Event to call when read data from USART

    dataValue = None

    aRoll = 0.3
    fRoll = 0.8

    aPitch = 0.2
    fPitch = 1.4

    aYaw = 0.08
    fYaw = 0.2
    mYaw = 0.05

    aLat = 0.00003
    fLat = 0.01
    mLat = 0.000002

    aLon = 0.00003
    fLon = 0.01
    mLon = 0.000001

    aAlt = 0.1
    fAlt = 0.2
    mAlt = 0.1

    receivedCommand = 0

    def __init__(self, logWriter):
        self.logWriter = logWriter
        self.onReceiveEvent = self.defaultOnReceiveEvent
      
        self.dataValue = DebugDataValue()
        self.dataValue.controllerState = 1000
        self.dataValue.battery = 10
        self.dataValue.flags = 10
        self.dataValue.CRC = 0

        self.aRoll += random.random() * (0.5 * self.aRoll)
        self.fRoll += random.random() * (0.5 * self.fRoll)

        self.aPitch += random.random() * (0.5 * self.aPitch)
        self.fPitch += random.random() * (0.5 * self.fPitch)

        self.aYaw += random.random() * (0.5 * self.aYaw)
        self.fYaw += random.random() * (0.5 * self.fYaw)
        self.mYaw += random.random() * (0.5 * self.mYaw)

        self.aLat += random.random() * (0.5 * self.aLat)
        self.fLat += random.random() * (0.5 * self.fLat)
        self.mLat += random.random() * (0.5 * self.mLat)

        self.aLon += random.random() * (0.5 * self.aLon)
        self.fLon += random.random() * (0.5 * self.fLon)
        self.mLon += random.random() * (0.5 * self.mLon)

        self.aAlt += random.random() * (0.5 * self.aAlt)
        self.fAlt += random.random() * (0.5 * self.fAlt)
        self.mAlt += random.random() * (0.5 * self.mAlt)

    #onReceiveEvent - call this function when new CommData is received via UART
    def setOnReceiveEvent(self, onReceiveEvent):
        self.onReceiveEvent = onReceiveEvent

    def defaultOnReceiveEvent(self, commData):
        self.logWriter.noteEvent('DroneSimulator: defaultOnReceiveEvent' + str(commData))

    def start(self):
        self.dataValue.lat = 50.0 + (random.random() - 0.5)
        self.dataValue.lon = 20.0 + (random.random() - 0.5)
        self.dataValue.alt = 40.0 + (random.random() - 0.5)*5

        self.simulatorThread = TimerThread('simulatorThread', self.simulatorThreadHandler, 0.2)
        self.simulatorThread.start()

    def close(self):
      print('DroneSimulator: close');
      if self.simulatorThread != None:
          self.simulatorThread.stop()


    def notifyCommData(self, commData):
        if (commData.typeString() == 'ControlData'):
            # process data as controller should do
            controlDataValue = commData.getValue()
            if controlDataValue.throttle > 0.03:
                self.receivedCommand = controlDataValue.controllerCommand
            else:
                self.receivedCommand = 0   
        elif (commData.typeString() == 'AutopilotData'):
            # respond with ACK (same data when success at changing target) as controller should do
            self.onReceiveEvent(commData)
        

    def simulatorThreadHandler(self):
        timeVal = time.time()

        self.dataValue.roll = math.sin(timeVal * self.fRoll) * self.aRoll; 
        self.dataValue.pitch = math.sin(timeVal * self.fPitch) * self.aPitch; 
        self.dataValue.yaw += math.sin(timeVal * self.fYaw) * self.aYaw + self.mYaw;

        if self.dataValue.yaw > 3.14:
            self.dataValue.yaw -= 2 * 3.14

        if self.dataValue.yaw < -3.14:
            self.dataValue.yaw += 2 * 3.14

        self.dataValue.lat += math.sin(timeVal * self.fLat) * self.aLat + self.mLat;
        self.dataValue.lon += math.sin(timeVal * self.fLon) * self.aLon + self.mLon;
        self.dataValue.alt += math.sin(timeVal * self.fAlt) * self.aAlt + self.mAlt;

        self.dataValue.controllerState = self.receivedCommand

        temp = DebugData(self.dataValue)
        self.dataValue.CRC = temp.computeCrc()
        debugMessage = DebugData(self.dataValue)

        self.onReceiveEvent(debugMessage)
       
        log_msg = 'DroneSimulator: DebugData: [' + str(debugMessage) + ']'
        self.logWriter.noteEvent(log_msg)
