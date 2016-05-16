#!/usr/bin/env python
from DroneControler import *
from IpController import *
from Settings import *
from LogWriter import *
from time import sleep
from traceback import format_exception
import signal,sys,os,threading
import getopt

closeServerApp = False # Main loop control (True=stop this app)

configFileName="ADdrone.cfg"
logsDIR="logs/"

###########################################################################
## LOAD SCRIPT ARGUMENTS
###########################################################################
customDIR="."
customPort=None

def help():
  print sys.argv[0]+' -d <dir> -p <portNum>'
  sys.exit(2)

try:
   argv=sys.argv[1:]
   opts, args = getopt.getopt(argv,"hd:p:",["daemon=","port="])
except getopt.GetoptError as err:
   print "ERROR: wrong args: ",err
   help()

for opt, arg in opts:
  if opt == '-h':
    help()
  elif opt in ("-d", "--deamon"):
    customDIR=str(arg)+"/"
    configFileName=customDIR+configFileName
    logsDIR=customDIR+"/"+logsDIR
  elif opt in ("-p", "--ofile"):
    customPort=int(arg)
  else:
    print "Error: unknown args"
    help()

if not os.path.isfile(configFileName):
  print "ERROR: can't find config file: "+str(configFileName)
  sys.exit(1)

if not os.path.exists(logsDIR):
  print "ERROR: can't find log dir: "+str(logsDIR)
  sys.exit(1)

###########################################################################
## LOAD SETTINGS
###########################################################################
SETTINGS = Settings(configFileName)
if customPort:
  SETTINGS.PORT=customPort

###########################################################################
## INIT
###########################################################################
#TODO make log writer global

logWriter = LogWriter(customDIR+"/logs/")

##UART part
droneController=DroneController(SETTINGS.UARTDEVICE, \
                                SETTINGS.UARTBAUDRATE, \
                                SETTINGS.UARTSIMULATOR, \
                                logWriter)
##-------

##IP part
server_name = ""  # "localhost"
ipController = IpController( (server_name, SETTINGS.PORT), \
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
#  print "MainThread: onReceiveUSART: [0x"+debugData.toStringHex()+"] "+str(debugData)
  ipController.send(debugData.data)

droneController.setOnReceiveEvent(onReceiveUSART)


def onReveiveControlDataFromIP(controlData):
  global droneController
#  print "MainThread: onReveiveControlDataFromIP: ' ",str(controlData),"'"
  droneController.setControlData(controlData)

ipController.setOnReceiveEvent(onReveiveControlDataFromIP)


###########################################################################
## MAIN LOOP
###########################################################################

if SETTINGS.TCPSIMULATOR == True:
    print('MainThread: Using port simulator')
else:
    print('MainThread: Using port number ' + str(SETTINGS.PORT))

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
