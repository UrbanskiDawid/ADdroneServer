from UartSender import *
from Message import *
import time

class DroneControler:
    uartSender = None

    def __init__(self, uartSender):
        self.uartSender = uartSender

    def newInstruction(self, message):

        msg=Message(message)
        if not msg.isValid():
          print "ERROR: wrong msg"
          return

        print time.strftime("%H:%M:%S"),str(msg)
        self.uartSender.send(message)
