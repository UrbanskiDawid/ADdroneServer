#!/usr/bin/env python
from DroneControler import *
from IpController import *
from Settings import *
from LogWriter import *
from time import sleep
import signal
import sys
import threading


###########################################################################
## LOAD SETTINGS
###########################################################################
SETTINGS = Settings()

if (len(sys.argv) == 2):
    SETTINGS.PORT = int(sys.argv[1])

server_name = ""  # "localhost"

if SETTINGS.TCPSIMULATOR == True:
    print('MainThread: Using port simulator')
else:
    print('MainThread: Using port number ' + str(SETTINGS.PORT))

server_address = (server_name, SETTINGS.PORT)

closeServerApp = False # Main loop control (True=stop this app)

###########################################################################
## INIT
###########################################################################
#TODO make log writer global

logWriter = LogWriter()

##UART part
def onReceiveUSART(msg):#DebugData
  global receiver
  receiver.send("debug:"+str(msg))
#  print "onReceiveUSART: ' ",msg,"'"

droneController=DroneController(onReceiveUSART, \
                                SETTINGS.UARTDEVICE, \
                                SETTINGS.UARTBAUDRATE, \
                                SETTINGS.UARTSIMULATOR, \
                                logWriter)
##-------

##IP part
def onReveiveControlDataFromIP(cd):#ControlData
  global droneController
  droneController.setControlData(cd)
#  print "onReveiveControlDataFromIP: ' ",cd.encode("hex"),"'"

receiver = IpController(onReveiveControlDataFromIP, \
                        server_address, \
                        SETTINGS.TCPSIMULATOR, \
                        True, \
                        SETTINGS.BINDRETRYNUM, \
                        logWriter)
##--

def endHandler(signal, frame):
  print('MainThread: end handler called')
  global closeServerApp
  global receiver
  global droneController
  logWriter.noteEvent("MainThread: endHandler");
  receiver.close()
  droneController.close()
  closeServerApp = True
  logWriter.close()
  sys.exit(0)


signal.signal(signal.SIGINT,  endHandler)
signal.signal(signal.SIGTERM, endHandler)

###########################################################################
## MAIN LOOP
###########################################################################
logWriter.noteEvent("MainThread: starting");

while not closeServerApp:
    print('MainThread: waiting for a connection')
    receiver.acceptConnection()
    while (receiver.keepConnection() and not closeServerApp):
        receiver.forwardIncomingPacket()
    receiver.close()
    print('MainThread: connection closed')

endHandler(None,None)
