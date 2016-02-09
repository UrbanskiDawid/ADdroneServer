from UartSender import *
from DroneControler import *
from IpReceiver import *


if (len(sys.argv) < 2):
    print ('Missing port number')
    sys.exit()
port_number = int(sys.argv[1])
server_name = ""  # "localhost"
server_address = (server_name, port_number)

uartSender = UartSender()
droneControler = DroneControler(uartSender)
receiver = IpReceiver(server_address, droneControler)

while True:
    print('waiting for a connection')
    receiver.acceptConnection()
    try:
        while True:
            receiver.forwardIncomingPacket()
    finally:
        connection.close()
