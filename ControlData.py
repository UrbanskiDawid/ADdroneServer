from struct import *
from CommData import *
from ControlDataValue import *
import sys

class ControlData(CommData):

    """ MESSAGE OVERRIDES """

    def typeString(self):
        return "ControlData"

    def getValue(self):
        return ControlDataValue(self)

    def toStringHex(self):
        i=0
        sep=[4,8,12,16,20,22,23,36]
        ret=''
        for b in self.data:
          if i in sep: ret+='|'
          ret+=b.encode('hex')
          i=i+1
        return ret

    """ CONTROL DATA SPECIFIC METHODS """

    def setErrorConnection(self):
        dataValue = self.getValue()
        dataValue.controllerCommand = 6100 # ERROR_CONNECTION
        self.data = dataValue.getData()
        dataValue.CRC = self.calculateCrc()
        self.data = dataValue.getData()
   
    @staticmethod
    def StopCommand():
        dataValue = ControlDataValue()
        dataValue.controllerCommand = 2000 # STOP
        dataValue.solverMode = 1 # STABLILIZATION
        dataValue.CRC = unpack("<H", "727a")[0] # CRC
        return ControlData(dataValue)

    @staticmethod
    def SomeValidControlCommand():
        dataValue = ControlDataValue()
        dataValue.throttle = 0.4
        dataValue.controllerCommand = 1000 # STOP
        dataValue.solverMode = 1 # STABLILIZATION
        dataValue.CRC = unpack("<H", "4588")[0] # CRC
        return ControlData(dataValue)
