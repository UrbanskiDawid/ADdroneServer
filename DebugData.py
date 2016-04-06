from struct import *
import sys

class DebugData:
    data = None
    valid = None
    
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
    
    def __init__(self, message):
        self.data = message
        self.valid = None
    
    def isValid(self):
        if self.valid is not None: #check only once
           return self.valid

        if self.data is None:
           sys.stderr.write('data = None\n')
           self.valid=False
           return False

        if len(self.data)!=38:
           sys.stderr.write('data len != 38\n')
           self.valid=False
           return False

        if self.data[0]!='$' or \
           self.data[1]!='$' or \
           self.data[2]!='$' or \
           self.data[3]!='$':
           sys.stderr.write('data wrong prefix: '+str(self.getPrefix())+'\n')
           self.valid=False
           return False
           
        #TODO: check CRC
        #if CRC is wrong
        #   sys.stderr.write('data wrong CRC\n')
        #   self.valid=False
        #   return False

        self.valid=True
        return True
        
    def toStringShort(self):
        tData = unpack(DebugData.messageFormat, self.data)
        return "(rpy: ({0:.2f},{1:.2f},{2:.2f}) state: {3:d} CRC: 0x{4:04X} )".format(
            tData[1], tData[2], tData[3],# roll, pitch, yaw
            tData[8], #controllerState
            tData[11]) #CRC


    def __str__(self):
        if not self.isValid():
            return "<DebugData> wrong data"
        return self.toStringShort()

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

