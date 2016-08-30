import sys
from struct import *

class CommData:
    data = None
    valid = None

    def __init__(self, data):
        from CommDataValue import CommDataValue
        if isinstance(data, str):
            self.data = data
        elif isinstance(data, CommDataValue):
            self.data = data.getCommData().data
        self.valid = None

    def computeCrc(self):
        crcShort = 0
        b = map(ord, self.data[4:-2])
        for byte in b:
            crcShort = ((crcShort >> 8) | (crcShort << 8) )& 0xffff
            crcShort ^= (byte & 0xff)
            crcShort ^= ((crcShort & 0xff) >> 4)
            crcShort ^= (crcShort << 12) & 0xffff
            crcShort ^= ((crcShort & 0xFF) << 5) & 0xffff
        crcShort &= 0xffff
        return crcShort

    def getData(self):
        return self.data

    def isValid(self):
        if self.valid is not None: #check only once
           return self.valid

        if self.data is None:
           sys.stderr.write(self.typeString() + ' data = None\n')
           self.valid=False
           return False

        if len(self.data) != self.getSize():
           sys.stderr.write(self.typeString() + ' data len != ' + str(self.getSize()) + '\n')
           self.valid=False
           return False

        if self.data[0]!=self.getPreamble() or \
           self.data[1]!=self.getPreamble() or \
           self.data[2]!=self.getPreamble() or \
           self.data[3]!=self.getPreamble():
           sys.stderr.write(self.typeString() + ' data wrong prefix\n')
           self.valid=False
           return False

        if self.computeCrc() != unpack("<H", self.data[-2:])[0]:
           sys.stderr.write(self.typeString() + ' data wrong CRC\n')
           self.valid=False
           return False

        self.valid=True
        return True

    def typeString():
        pass

    def getValue(self):
        pass

    def getSize(self):
        pass

    def getPreamble(self):
        pass

    def toStringHex(self):
        i = 0
        sep = [4,8,12,16,20,24,28,32,36]
        ret = ''
        for b in self.data:
          if i in sep: 
            ret += '|'
          ret += b.encode('hex')
          i = i + 1
        return ret

    def toStringValue(self):
        return self.getValue().toString() 

    def __str__(self):
     if not self.isValid():
       return "<", self.typeString(), "> wrong data"
     return self.toStringValue()

    def __bool__(self):
        return self.isValid()
    __nonzero__=__bool__
