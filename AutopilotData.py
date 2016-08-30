from struct import *
from CommData import *

class AutopilotData(CommData):

    """ MESSAGE OVERRIDES """

    def typeString(self):
        return "AutopilotData"

    def getValue(self):
        from AutopilotDataValue import AutopilotDataValue
        return AutopilotDataValue(self)

    def getSize(self):
        return 30

    def getPreamble(self):
        return '^'

    def toStringHex(self):
        i=0
        sep=[4,12,20,24,28]
        ret=''
        for b in self.data:
          if i in sep: ret+='|'
          ret+=b.encode('hex')
          i=i+1
        return ret
