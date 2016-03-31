from struct import *
import sys

class DebugData:
    data = None
    valid = None
    
    # message struct
    messageFormat='<'\
                  'cccc'\
                  'fffffff'\
                  'H'\
                  'BB'\
                  'H'
    
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
        tData=unpack(self.messageFormat,self.data)
        return "(rpy: {0:.2f},{1:.2f},{2:.2f}, state: {3:d} )".format(
            tData[4],
            tData[5],
            tData[6],
            tData[11] )

    def __str__(self):
        if not self.isValid():
            return "<DebugData> wrong data"
        return self.toStringShort()
