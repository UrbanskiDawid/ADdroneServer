from struct import *
import sys

class Message:
    stringData = None  # string
    byteData = None    # bytes-like
    valid = None

    # message struct
    messageFormat = ('<'
                     'cccc'          #  4 bytes
                     'ffff'          # 16 bytes
                     'H'             #  2 bytes
                     'B'             #  1 bytes
                     'ccccccccccccc' # 13 bytes
                     'H')            #  2 bytes
    #SEE: https://docs.python.org/2/library/struct.html
    #
    #  !	network (= big-endian)	
    #  <        little-endian
    #
    #Format	C Type		Python type		Standard size
    #  c	char		string of length 	1
    #  f	float		float			4
    #  H	unsigned short	integer			2

    def __init__(self, stringMessage):
        self.byteData = str.encode(stringMessage)
        self.stringData = stringMessage
        self.calcValid()
        # self.valid = None

    def isValid(self):
        return self.valid

    def calcValid(self):
        if self.byteData is None:
            sys.stderr.write('data = None\n')
            self.valid = False
            return False

        if len(self.stringData) != 38:
            sys.stderr.write('data len != 38\n')
            self.valid = False
            return False

        if self.stringData[0] != '$' or \
           self.stringData[1] != '$' or \
           self.stringData[2] != '$' or \
           self.stringData[3] != '$':
            sys.stderr.write('data wrong prefix: '+str(self.getPrefix())+'\n')
            self.valid = False
            return False

        #TODO: check CRC
        #if CRC is wrong
        #   sys.stderr.write('data wrong CRC\n')
        #   self.valid=False
        #   return False

        self.valid = True
        return True
     
    def toStringAll(self):
        return str(unpack(self.messageFormat, self.byteData))

    def toStringHex(self):#24242424|00000000|00000000|00000000|85f6123f|e803|0a|ffffffffffffffffffffffffff|9ea6
        sep=[4,8,12,16,20,22,23,36]
        ret=''
        for i in range(len(self.byteData)):
            if i in sep:
                ret += '|'
            ret += bytearray([self.byteData[i]]).hex()
        return ret

    def toStringShort(self):
        tData = unpack(self.messageFormat, self.byteData)
        return "(analogs: {0:.2f},{1:.2f},{2:.2f},{3:.2f} cmd: {4:d} solverModeStabilization: {5:d} CRC: 0x{5:02X})".format(
            tData[4],
            tData[5],
            tData[6],
            tData[7],
            tData[8],
            tData[9],
            tData[23])

    def __str__(self):
        if not self.isValid():
            return "<Message> wrong data"
        return self.toStringShort()

    def getPrefix(self):
        return self.stringData[:4]
