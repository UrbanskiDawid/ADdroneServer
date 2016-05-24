from struct import *
from CommData import *
from ControlDataValue import *
import sys

class ControlData(CommData):

    # message struct
    messageFormat='<'\
                  '4s'\
                  '4f'\
                  'H'\
                  'B'\
                  '13s'\
                  'H'
    # example: ('$$$$', 0.0, 0.0, 0.0, 0.0, 1000, 10, 1, 65535)
    # '<'         encoding = network = big endian
    # 0     '4s'        # preamble $$$$
    # 1,2,3 '3f'        # roll, pitch, yaw
    # 4     'f'         # throtthe
    # 6     'H'         # controller command
    # 7     'B'         # solver mode
    # 8     '13s'       # dummy 
    # 9     'H'         # crc

    """ MESSAGE OVERRIDES """

    def typeString(self):
        return "ControlData"

    def getValue(self):
        return ControlDataValue(self)

    #24242424|00000000|00000000|00000000|85f6123f|e803|0a|ffffffffffffffffffffffffff|9ea6
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
        tData = unpack(ControlData.messageFormat, self.data)      
        # 6100 - ERROR_CONNECTION
        newData = pack(ControlData.messageFormat, tData[0], tData[1], tData[2], 
            tData[3], tData[4], 6100, tData[6], tData[7], tData[8])
        # TODO recalculate CRC
        newCrc = self.calculateCrc(newData)
        self.data = pack(ControlData.messageFormat, tData[0], tData[1], tData[2], 
            tData[3], tData[4], 6100, tData[6], tData[7], newCrc)

    # TODO - to be refactored with usage of ControlDataValue class   
    @staticmethod
    def StopCommand():
        data = pack(ControlData.messageFormat,
                    "$$$$",
                    0.0, 0.0, 0.0, 0.0, #roll pith yaw throttle
                    2000,               # cmd
                    1,                  # solver mode
                    "\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff",    #padding
                    0x727a)             #crc
        return ControlData(data)

    @staticmethod
    def SomeValidControlCommand():
        data = pack(ControlData.messageFormat,
                    "$$$$",
                    0.0, 0.0, 0.0, 0.4, #roll pith yaw throttle
                    1000,               # cmd
                    1,                  # solver mode
                    "\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff",    #padding
                    0x4588)             #crc
        return ControlData(data)
