from struct import *
import sys

class Message:
    data=None
    valid=None

    #message struct
    messageFormat='!'\
                  'cccc'\
                  'ffff'\
                  'H'\
                  'cccccccccccccc'\
                  'H'
    #SEE: https://docs.python.org/2/library/struct.html
    #
    #  !	network (= big-endian)	
    #
    #Format	C Type		Python type		Standard size
    #  c	char		string of length 	1
    #  f	float		float			4
    #  H	unsigned short	integer			2

    def __init__(self, message):
        self.data = message
        self.valid = None

    def __bool__(self):
        return self.isValid()
    __nonzero__=__bool__

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

    def getPrefixInt(self): #int array
        return [ord(self.data[0]),ord(self.data[1]),ord(self.data[2]),ord(self.data[3])]

    def getPrefix(self): #int array
        return unpack('cccc', self.data[ 3]+self.data[ 2]+self.data[ 1]+self.data[ 0])

    def getCRC(self):
        return struct.unpack('f', bytes([self.data[30],self.data[29],self.data[28],self.data[27]]))[0]

    def toStringAll(self):
        return str(unpack(self.messageFormat,self.data))

    def toStringShort(self):
        tData=unpack(self.messageFormat,self.data)
        return "(axis1: {0:.2f},{1:.2f} axis2: {2:.2f},{3:.2f} cmd: 0x{4:02X} CRC: 0x{5:02X})".format( 
            tData[4],
            tData[5],
            tData[6],
            tData[7],
            tData[8],
            tData[23]   )

    def __str__(self):
     if not self.isValid():
       return "<Message> wrong data"
     return self.toStringShort()
