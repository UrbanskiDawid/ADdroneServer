#!/usr/bin/env python
from FakeUartSender import *
from     UartSender import *
from DroneControler import *
from IpReceiver import *
from Settings import *
from LogWriter import *
from time import sleep
import signal
import sys
import threading

SETTINGS = Settings()

if (len(sys.argv) == 2):
    SETTINGS.PORT = int(sys.argv[1])

server_name = ""  # "localhost"

if SETTINGS.SIMULATOR == True:
    print('Using port simulator')
else:
    print('Using port number ' + str(SETTINGS.PORT))

server_address = (server_name, SETTINGS.PORT)

if SETTINGS.UARTSIMULATOR == True:
    uartSender = FakeUartSender()
else:
    uartSender = UartSender(SETTINGS.UARTDEVICE, SETTINGS.UARTBAUDRATE)

closeServerApp = False

#TODO make log writer global
logWriter = LogWriter()
droneControler = DroneControler(uartSender, logWriter)
receiver = IpReceiver(server_address, SETTINGS.SIMULATOR, True, droneControler, \
                      SETTINGS.BINDRETRYNUM, \
                      logWriter)
droneControler.setIpConnection(receiver)

heartBeatAlive=True
def heartBeat():
  global heartBeatAlive
  global receiver
  while heartBeatAlive:
    sleep(2)
    if receiver.keepConnection():
      receiver.send("tick")

t1 = threading.Thread(target=heartBeat)
t1.start()

def end_handler(signal, frame):
  print('end handler called')
  global closeServerApp
  global receiver
  receiver.keepConnectionFlag = False
  closeServerApp = True

signal.signal(signal.SIGINT,  end_handler)
signal.signal(signal.SIGTERM, end_handler)

while not closeServerApp:
    print('waiting for a connection')
    receiver.acceptConnection()
    while (receiver.keepConnection() and not closeServerApp):
        receiver.forwardIncomingPacket()
    receiver.closeConnection()
    print('connection closed')

print('exiting')
heartBeatAlive = False
t1.join()
sys.exit(0)
