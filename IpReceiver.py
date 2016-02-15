import socket
import sys


class IpReceiver:
    sock = None
    connection = None
    droneControler = None

    def __init__(self, server_address, droneControler):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(server_address)
        self.sock.listen(1)
        self.droneControler = droneControler

    def acceptConnection(self):
        self.connection, client_address = self.sock.accept()
        print(sys.stderr, 'client connected:', client_address)

    def forwardIncomingPacket(self):
        BUFFER_SIZE = 16384
        data = self.connection.recv(BUFFER_SIZE)
        if data:
            self.droneControler.newInstruction(data)
        else:
            print('connection closed');
            self.closeConnection()

    def closeConnection(self):
        self.sock.close()
