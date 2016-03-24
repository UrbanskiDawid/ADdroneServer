#!/usr/bin/env python
from FakeUartSender import *
from UartSender import *
from DroneControler import *
from IpReceiver import *
from Settings import *
from LogWriter import *
from time import sleep
import signal
import sys
import threading

def end_handler(_signal, frame):
    print('exiting!')

    global receiver
    receiver.closeConnection()

    global heartBeatAlive
    heartBeatAlive = False
    threadHeartBeat.join()
    sys.exit(0)

def heartBeat():
    global heartBeatAlive
    global receiver
    while heartBeatAlive:
        sleep(2)
        if receiver.keepConnection():
            receiver.send("tick")

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

logWriter = LogWriter()
droneControler = DroneControler(uartSender, logWriter)
receiver = IpReceiver(server_address, SETTINGS.SIMULATOR, droneControler, \
                      SETTINGS.BINDRETRYNUM, \
                      logWriter)

heartBeatAlive = True
threadHeartBeat = threading.Thread(target=heartBeat)
threadHeartBeat.start()

signal.signal(signal.SIGINT,  end_handler)
signal.signal(signal.SIGTERM, end_handler)

while True:
    print('waiting for a connection')
    receiver.acceptConnection()
    while receiver.keepConnection():
        receiver.forwardIncomingPacket()
