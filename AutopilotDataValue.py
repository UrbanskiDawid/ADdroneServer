from struct import *
from CommDataValue import CommDataValue
from AutopilotData import AutopilotData

class AutopilotDataValue(CommDataValue):

    # control communication data struct
    messageFormat = '<4s2dfiH'
    # example: ('$$$$', 50.00, 20.00, 12.0, 0, 65535)
    # '<'         encoding = network = big endian
    # 0     '4s'        # preamble $$$$
    # 1,2   '2d'        # lat, lon
    # 3     'f'         # alt
    # 4     'i'         # flags
    # 5     'H'         # crc

    lat = 0.0
    lon = 0.0
    alt = 0.0

    flags = 0
    
    def __init__(self, controlData = None):
        self.preamble = "^^^^"
        if controlData is not None:
            values = unpack(self.messageFormat, controlData.getData()) 
            self.preamble = values[0]
            self.lat = values[1]
            self.lon = values[2]
            self.alt = values[3]
            self.flags = values[4]
            self.CRC = values[5]

    def getCommData(self):
        data = pack(self.messageFormat,
            self.preamble, 
            self.lat, 
            self.lon,
            self.alt,
            self.flags,
            self.CRC)
        return AutopilotData(data)

    def toString(self):
        return "(rpy: ({0:.5f},{1:.5f},{2:.2f}), flags: {3:d}, CRC: 0x{4:04X})".format(
            self.lat, self.lon,
            self.alt,
            self.flags,
            self.CRC)
