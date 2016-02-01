import socket
import sys
import struct
from Message import *
from UartSender import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = "" # "localhost"
if (len(sys.argv) < 2):
  print ('Missing port number')
  sys.exit()

port_number = int(sys.argv[1])
server_address = (server_name, port_number)

sock.bind(server_address)
sock.listen(1)

sender = UartSender()

while True:
  print('waiting for a connection')
  connection, client_address = sock.accept()
  try:
    print(sys.stderr, 'client connected:', client_address)
    while True:
      data=connection.recv(256)
      message = Message(data)
      if data:
        if not message.isValidCommand():
          print('received garbage "%s"' % data)
        sender.sendMessage(data)
        connection.sendall(data)
      else:
        print('connection closed');
        connection.close()
        break;
  finally:
    connection.close()