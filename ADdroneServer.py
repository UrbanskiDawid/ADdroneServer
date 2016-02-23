#!/usr/bin/env python
from FakeUartSender import *
from DroneControler import *
from IpReceiver import *
from Settings import *
from LogWriter import *
import time
import signal
import sys

SETTINGS = Settings()

if (len(sys.argv) == 2):
    SETTINGS.PORT = int(sys.argv[1])

if SETTINGS.PORT==False:
    print ('missing port')
    sys.exit()

print ('Using port number '+str(SETTINGS.PORT))


server_name = ""  # "localhost"
server_address = (server_name, SETTINGS.PORT)

uartSender = FakeUartSender()
droneControler = DroneControler(uartSender)
logWriter = LogWriter()
receiver = IpReceiver(server_address, droneControler, \
                      SETTINGS.BINDRETRYNUM, \
                      logWriter)

def signal_handler(signal, frame):
  print('You pressed Ctrl+C!')
  receiver.closeConnection();
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

while True:
    print('waiting for a connection')
    receiver.acceptConnection()
    while receiver.keepConnection():
        receiver.forwardIncomingPacket()
