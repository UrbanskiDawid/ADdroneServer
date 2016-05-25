from struct import *
from CommData import *
import sys

class DebugData(CommData):
        
    """ MESSAGE OVERRIDES """

    def typeString(self):
        return "DebugData"

    def getValue(self):
        from DebugDataValue import DebugDataValue
        return DebugDataValue(self)

    def toStringHex(self):
        i=0
        sep=[4,8,12,16,20,24,28,32,34,35,36]
        ret=''
        for b in self.data:
          if i in sep: ret+='|'
          ret+=b.encode('hex')
          i=i+1
        return ret

    """ DEBUG DATA SPECIFIC METHODS """

    def setConnectionLost(self):
        pass

    @staticmethod
    def SomeValidControlCommand():
        from DebugDataValue import DebugDataValue
        dataValue = DebugDataValue()
        dataValue.controllerState = 1000 # STOP
        dataValue.battery = 10
        dataValue.flags = 10
        dataValue.CRC = unpack("<H", "65535")[0] # CRC
        return DebugData(dataValue)
