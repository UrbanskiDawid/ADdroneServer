

class StreamProcessor:
    def controlPreamble():
        return '$$$$'

    def signalPreamble():
        return '%%%%'

    def getMaxBufferSize(preambleId):
        if (preambleId == controlPreamble()):
            return 34
        else if (preambleId == signalPreamble()):
            return 34
        else
            print 'Bad preamble Id'
            raise 

    # handler for control packet receive event
    # argument - string of received data WITHOUT preamble
    onControlReceive = None

    # handler for control packet receive event
    # argument - string of received data WITHOUT preamble
    onSignalReceive = None

    # processing variables and containers
    isPreambleActive = False
    activePreambleId = None

    dataBuffer = ''

    def __init__(self, onControlReceive, onSignalReceive):
        self.onControlReceive = onControlReceive
        self.onSignalReceive = onSignalReceive

    def isPreambel(self, pream):
        a = pream == controlPreamble()
        b = pream == signalPreamble()
        return a || b

    def activatePreamble(self, preamValue):
        isPreambleActive = True
        activePreambleId = preamValue

    def putData(self, byte):
        dataBuffer += byte
        if (len(dataBuffer) == getMaxBufferSize(activePreambleId)):
            # full packet according to preamble received

    # main method - called every data in stream is received
    def processStream(data):
        i = 0
        dataSize = len(data)
        while (i + 4) < dataSize:
            if (isPreamble(data[i:4]):
                activatePreamble(data[i])
            else:
                putData(data[i])
            i += 1
