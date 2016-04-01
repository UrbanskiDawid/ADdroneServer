from struct import *
import sys

class ControlData:
    data = None
    valid = None
    
    # message struct
    messageFormat='<'\
                  '4s'\
                  '4f'\
                  'H'\
                  'B'\
                  '13s'\
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
        
    def toStringShort(self):
        tData=unpack(ControlData.messageFormat, self.data)
        return "(analogs: {0:.2f},{1:.2f},{2:.2f},{3:.2f} cmd: {4:d} mode: {5:d} CRC: 0x{5:02X})".format(
            tData[1],
            tData[2],
            tData[3],
            tData[4],
            tData[5],
            tData[6],
            tData[8])

    def __str__(self):
        if not self.isValid():
            return "<ControlData> wrong data"
        return self.toStringShort()
        
    @staticmethod
    def StopCommand():
        data = "24242424" # preamble
        data += "00000000" # roll = 0.0f
        data += "00000000" # pitch = 0.0f
        data += "00000000" # yaw = 0.0f
        data += "00000000" # throttle = 0.0f
        data += "d007" # command = 2000
        data += "0a" # solver mode
        while len(data) < 36 * 2:
            data += "f" # padding
        data += "ffff" # CRC   
        return ControlData(data.decode("hex"))

    @staticmethod
    def SomeValidControlCommand2():
        data = "24242424" # preamble
        data += "00000000" # roll = 0.0f
        data += "00000000" # pitch = 0.0f
        data += "00000000" # yaw = 0.0f
        data += "00000000" # throttle = 0.0f
        data += "e803" # command = 1000
        data += "0a" # solver mode
        while len(data) < 36 * 2:
            data += "f" # padding
        data += "ffff" # CRC   
        return ControlData(data.decode("hex"))

    @staticmethod
    def SomeValidControlCommand():
        data = pack(ControlData.messageFormat,
                    "$$$$",
                    0.0, 0.0, 0.0, 0.0, #roll pith yaw throttle
                    1000,               # cmd
                    10,                 # solver mode
                    "\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff",    #padding
                    65535)              #crc

        if ControlData.SomeValidControlCommand2().data != data:
            print "ERROR: invalid data. data : ", data.encode("hex"), "\n"
            print "ERROR l2 Command2 : ", ControlData.SomeValidControlCommand2().data.encode("hex")
            return ""
        return ControlData(data)
