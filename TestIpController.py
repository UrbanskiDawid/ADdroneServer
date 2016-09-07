from IpController import *
from LogWriter import *

logWriter = LogWriter('logs/')

receiver = IpController('',
                        True,
                        False,
                        10,
                        logWriter)


def onReveiveControlDataFromIP(controlData):
    print "MainThread: ", str(controlData)

receiver.setOnReceiveEvent(onReveiveControlDataFromIP)


print('MainThread: waiting for a connection')
receiver.acceptConnection()
while receiver.keepConnection():
    receiver.forwardIncomingPacket()
print('MainThread: connection closed')

logWriter.noteEvent("MainThread: endHandler")
receiver.close()
logWriter.close()

print "DONE"
