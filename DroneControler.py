from UartSender import *
from struct import *

class DroneControler:
    uartSender = None

    #message struct
    messageFormat='cccc'\
                  'ffff'\
                  'H'\
                  'cccccccccccccc'\
                  'H'
    #SEE: https://docs.python.org/2/library/struct.html

    def __init__(self, uartSender):
        self.uartSender = uartSender

    def newInstruction(self, message):
        errStr=""
        if message[0]!='$':    errStr+="wrong prefix "
        if len(message)!=38:   errStr+="wrong length "+str(len(message))+" "
        if errStr!="":
          print "ERROR: FakeUartSender send()"+errStr
          return
        print( unpack(self.messageFormat,message) 
        self.uartSender.send(message)
