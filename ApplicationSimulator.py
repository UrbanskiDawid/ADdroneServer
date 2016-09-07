#!/usr/bin/env python

from DroneSimulator import *
from IpController import *
from LogWriter import *
from TimerThread import *
from ZTEmodem import *

from traceback import format_exception
import signal, sys

closeServerApp = False # Main loop control (True=stop this app)

customDir="."

logWriter = LogWriter(customDir + "/logs/simulator")


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

def endHandler(signal, frame):
    print('MainThread: end handler called')
    global closeServerApp
    global droneSimulator
    global ipController
    logWriter.noteEvent("MainThread: endHandler")
    droneSimulator.close()
    ipController.close()
    closeServerApp = True
    logWriter.close()
    sys.exit(0)

sys.excepthook = topExceptHook

signal.signal(signal.SIGINT, endHandler)
signal.signal(signal.SIGTERM, endHandler)



droneSimulator = DroneSimulator(logWriter)

serverName = ""  # "localhost"
serverPort = 6666

ipController = IpController((serverName, serverPort), False, False, 5, logWriter)



# handler for DroneSimulator onReceiveEvent
# forwards valid CommData to IpController
def onReceiveCommDataFromSymulator(commData):
    global ipController
    print "Sending: " + str(commData)
    ipController.sendCommData(commData.data)

droneSimulator.setOnReceiveEvent(onReceiveCommDataFromSymulator)

# hanlder for IpController onReceiveEvent
# forwards calid CommData to DroneSimulator
def onReveiveCommDataFromIp(commData):
    global droneSimulator
    print "Received: " + str(commData)
    droneSimulator.notifyCommData(commData)

ipController.setOnReceiveEvent(onReveiveCommDataFromIp)



# main loop
while not closeServerApp:
    print('MainThread: waiting for a connection')
    ipController.acceptConnection()
    droneSimulator.start()
    while ipController.keepConnection() and not closeServerApp:
        ipController.forwardIncomingPacket()
    droneSimulator.close()
    print('MainThread: connection closed')

endHandler(None,None)
