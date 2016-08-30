from struct import *
from CommData import *

class ControlData(CommData):

    """ MESSAGE OVERRIDES """

    def typeString(self):
        return "ControlData"

    def getValue(self):
        from ControlDataValue import ControlDataValue
        return ControlDataValue(self)

    def getSize(self):
        return 38

    def getPreamble(self):
        return '$'

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
        self.data = dataValue.getCommData().data
        dataValue.CRC = self.computeCrc()
        self.data = dataValue.getCommData().data
   
    @staticmethod
    def StopCommand():
        from ControlDataValue import ControlDataValue
        dataValue = ControlDataValue()
        dataValue.controllerCommand = 2000 # STOP
        dataValue.solverMode = 1 # STABLILIZATION
        dataValue.CRC = 0
        temp = ControlData(dataValue)
        dataValue.CRC = temp.computeCrc()
        return ControlData(dataValue)

    @staticmethod
    def SomeValidControlCommand():
        from ControlDataValue import ControlDataValue
        dataValue = ControlDataValue()
        dataValue.throttle = 0.4
        dataValue.controllerCommand = 1000 # STOP
        dataValue.solverMode = 1 # STABLILIZATION
        dataValue.CRC = 0
        temp = ControlData(dataValue)
        dataValue.CRC = temp.computeCrc()
        return ControlData(dataValue)
