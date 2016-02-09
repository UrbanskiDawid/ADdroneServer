from UartSender import *


class DroneControler:
    uartSender = None

    def __init__(self, uartSender):
        self.uartSender = uartSender

    def newInstruction(self, message):
        self.uartSender.send(message)
