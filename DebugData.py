from struct import *
from CommData import *
import sys

class DebugData(CommData):
   
    # message struct
    messageFormat = ('<4s3f3ffHBBH')
    # example: ('$$$$', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1000, 10, 10, 65535)
    # '<'         encoding = network = big endian
    # 0     '4s'        # preamble $$$$
    # 1,2,3 '3f'        # roll, pitch, yaw
    # 4,5,6 '3f'        # lat, lon, alt
    # 7     'f'         # speed
    # 8     'H'         # controllerState
    # 9     'BB'        # battery(tricky), flags(GPS fix | GPS 3D fix | low bat. vol. | nu | nu | nu | solver1 | solver2
    # 6     'H'         # crc
        
    """ MESSAGE OVERRIDES """

    def typeString(self):
        return "DebugData"

    def getValue(self):
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

    # TODO - to be refactored with usage of ControlDataValue class 
    @staticmethod
    def SomeValidDebugData():
        data = pack(DebugData.messageFormat,
                    "$$$$",
                    0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0,
                    0.0,
                    1000,   # ctrl state
                    10,     # bat
                    10,     # flags
                    65535)  # crc fake
        return DebugData(data)

