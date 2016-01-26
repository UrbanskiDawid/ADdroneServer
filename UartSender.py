import serial

class UartSender:
  def sendMessage(self, message):
    connection = serial.Serial ("/dev/ttyAMA0") 
    connection.baudrate = 9600 
    connection.write("Hello") 
    connection.close()