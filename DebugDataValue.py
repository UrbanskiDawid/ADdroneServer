from struct import *
from CommDataValue import CommDataValue
from DebugData import DebugData

class DebugDataValue(CommDataValue):

    # debug communication data struct
    messageFormat = ('<4s3f3ffHBBH')
    # example: ('$$$$', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1000, 10, 10, 65535)
    # '<'         encoding = network = big endian
    # 0     '4s'        # preamble $$$$
    # 1,2,3 '3f'        # roll, pitch, yaw
    # 4,5,6 '3f'        # lat, lon, alt
    # 7     'f'         # speed
    # 8     'H'         # controllerState
    # 9,10  'BB'        # battery(tricky), flags(GPS fix | GPS 3D fix | low bat. vol. | nu | nu | nu | solver1 | solver2
    # 11     'H'         # crc

    roll = 0.0
    pitch = 0.0
    yaw = 0.0

    lat = 0.0
    lon = 0.0
    alt = 0.0
    speed = 0.0

    controllerState = 0
    battery = 0
    flags = 0

    def __init__(self, debugData = None):
        self.preamble = "$$$$"
        if controlData is not None:
            values = unpack(self.messageFormat, debugData.getData()) 
            self.preamble = values[0]
            self.roll = values[1]
            self.pitch = values[2]
            self.yaw = values[3]
            self.lat = values[4]
            self.lon = values[5]
            self.alt = values[6]
            self.speed = values[7]
            self.controllerState = values[8]
            self.battery = values[9]
            self.flags = values[10]
            self.CRC = values[11]

    def getCommData(self):
        data = pack(ControlData.messageFormat,
            self.preamble, 
            self.roll, self.pitch, self.yaw,
            self.throttle,
            self.controllerCommand,
            self.solverMode,
            "\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff", # padding
            self.CRC)
        return ControlData(data)

    def toString(self):
        return "(rpy: ({0:.2f},{1:.2f},{2:.2f}), th: {3:.2f}, cmd: {4:d} CRC: 0x{5:04X})".format(
            self.roll, self.pitch, self.yaw,
            self.throttle
            self.controllerCommand,
            self.CRC)
