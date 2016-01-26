import socket
import sys
from base64 import *
import struct
from MessageDecoder import *
from UartSender import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = ""#"localhost"
server_address = (server_name, 1234)

sock.bind(server_address)
sock.listen(1)

decoder = MessageDecoder()
sender = UartSender()

while True:
  print('waiting for a connection')
  connection, client_address = sock.accept()
  try:
    print(sys.stderr, 'client connected:', client_address)
    while True:
      data=connection.recv(256)
      if data:
        if not decoder.tryToReadMessage(data):
          print('received garbage "%s"' % data)
        sender.sendMessage('Hello, UART!') 
        connection.sendall(data)
      else:
        print('connection closed');
        connection.close()
        break;
  finally:
    connection.close()