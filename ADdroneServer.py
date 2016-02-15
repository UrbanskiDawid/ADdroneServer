from FakeUartSender import *
from DroneControler import *
from IpReceiver import *
import time


if (len(sys.argv) < 2):
    print ('Missing port number')
    sys.exit()

port_number = int(sys.argv[1])
server_name = ""  # "localhost"
server_address = (server_name, port_number)

uartSender = FakeUartSender()
droneControler = DroneControler(uartSender)
receiver = IpReceiver(server_address, droneControler)

while True:
    print('waiting for a connection')
    receiver.acceptConnection()
    while receiver.keepConnection():
        receiver.forwardIncomingPacket()
    time.sleep(5)
