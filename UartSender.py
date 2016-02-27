import serial


class UartSender:
    connection = None

    def __init__(self,device,baundRate):
        self.connection = serial.Serial(device)
        self.connection.baudrate = baundrate
        print "UartSender constructed (", device, " at ",baundRate,")"

    def send(self, message):
        self.connection.write(message)

    def closeConnection(self):
        self.connection.close()
