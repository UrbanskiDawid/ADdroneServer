import sys
from Message import *
from UartSender import *
from IpReceiver import *

if (len(sys.argv) < 2):
  print ('Missing port number')
  sys.exit()
port_number = int(sys.argv[1])
server_name = "" # "localhost"
server_address = (server_name, port_number)

receiver = IpReceiver(server_address)
sender = UartSender()

while True:
  print('waiting for a connection')
  receiver.acceptConnection()
  try:
    while True:
      data = receiver.receive()
      if data:
        message = Message(data)
        message.sendOnUart(sender)
      else:
        print('connection closed');
        receiver.close()
        break;
  finally:
    connection.close()
