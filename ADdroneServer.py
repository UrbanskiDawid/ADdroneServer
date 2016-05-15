#!/usr/bin/env python
from DroneControler import *
from IpController import *
from Settings import *
from LogWriter import *
from time import sleep
import signal
import sys
import os
import threading
from traceback import format_exception

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
droneController=DroneController(SETTINGS.UARTDEVICE, \
                                SETTINGS.UARTBAUDRATE, \
                                SETTINGS.UARTSIMULATOR, \
                                logWriter)
##-------

##IP part
ipController = IpController(server_address, \
                        SETTINGS.TCPSIMULATOR, \
                        True, \
                        SETTINGS.BINDRETRYNUM, \
                        logWriter)
##--

###########################################################################
## EVENTS
###########################################################################
def endHandler(signal, frame):
  print('MainThread: end handler called')
  global closeServerApp
  global ipController
  global droneController
  logWriter.noteEvent("MainThread: endHandler");
  ipController.close()
  droneController.close()
  closeServerApp = True
  logWriter.close()
  sys.exit(0)

signal.signal(signal.SIGINT,  endHandler)
signal.signal(signal.SIGTERM, endHandler)

def topExceptHook(type, value, traceback):
  global logWriter
  exceptMsg=format_exception(type, value, traceback)
  try:
    logWriter.noteEvent("MainThread: unhandled Exception ",str(exceptMsg))
  except:
    pass #can't handle logWriter exceptions here

  print "MainThread: unhandled Exception "
  for line in format_exception(type, value, traceback):
    print line,

  endHandler(None,None)

sys.excepthook = topExceptHook


def onReceiveUSART(debugData):#DebugData
  global ipController
  ipController.send(debugData)
#  print "MainThread: onReceiveUSART: ' ",debugData,"'"

droneController.setOnReceiveEvent(onReceiveUSART)


def onReveiveControlDataFromIP(controlData):
  global droneController
  droneController.setControlData(controlData)
#  print "MainThread: onReveiveControlDataFromIP: ' ",str(controlData),"'"

ipController.setOnReceiveEvent(onReveiveControlDataFromIP)


###########################################################################
## MAIN LOOP
###########################################################################
log_msg="MainThread: starting"+str(os.getpid())
logWriter.noteEvent(log_msg);
print log_msg

while not closeServerApp:
    print('MainThread: waiting for a connection')
    ipController.acceptConnection()
    while (ipController.keepConnection() and not closeServerApp):
        ipController.forwardIncomingPacket()
    print('MainThread: connection closed')

endHandler(None,None)
