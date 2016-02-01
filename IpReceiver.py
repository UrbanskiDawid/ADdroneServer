import socket

class IpReceiver:
  sock = None
  connection = None

  def __init__(self, server_address):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind(server_address)
    self.sock.listen(1)

  def acceptConnection(self):
    connection, client_address = self.sock.accept()
    print(sys.stderr, 'client connected:', client_address)

  def receive(self):
    bufferSize = 256
    data = connection.recv(bufferSize)
    return data

  def closeConnection(self):
    sock.close()