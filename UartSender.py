import serial

class UartSender:
    connection = None;
    message = None;

    def __init__(self):
        self.connection = serial.Serial("/dev/ttyAMA0")
        self.connection.baudrate = 9600

    def updateMessage(self, message):
        self.message = message
        self.sendMessage()

    def sendMessage(self):
        self.connection.write(self.message)

    def closeConnection(self):
        self.connection.close()
