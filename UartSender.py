import serial


class UartSender:
    connection = None

    def __init__(self):
        self.connection = serial.Serial("/dev/ttyAMA0")
        self.connection.baudrate = 9600

    def send(self, message):
        self.connection.write(message)

    def closeConnection(self):
        self.connection.close()
