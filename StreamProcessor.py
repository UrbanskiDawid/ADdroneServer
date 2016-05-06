

class StreamProcessor:
    @staticmethod
    def controlPreamble():
        return '$$$$'

    @staticmethod
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
        a = (pream == self.controlPreamble())
        b = (pream == self.signalPreamble())
        return a || b

    def activatePreamble(self, preamValue):
        self.isPreambleActive = True
        self.activePreambleId = preamValue

    def putData(self, byte):
        dataBuffer += byte
        if (len(dataBuffer) == getMaxBufferSize(activePreambleId)):
            # full packet according to preamble received
            self.onReceive();
            # cleanup for next reception
            isPreambleActive = False
            activePrembleId = None
            dataBuffer = ''

    # main method - called every data in stream is received
    def processStream(self, data):
        i = 0
        dataSize = len(data)
        while (i < dataSize):
            # check for preamble
            if (i + 4 > dataSize && self.isPreamble(data[i:4]):
                self.activatePreamble(data[i])
            # else try to put byte into buffer if preable is received
            else if (self.isPreambleActive):
                self.putData(data[i])
            i += 1

    def onReceive(self):
        if (self.activePreambleId == self.controlPreamble()):
            self.onControlReceive(self.controlPreamble() + dataBuffer)
        else if (self.activePreambleId == self.signalPreamble()):
            self.onSignalReceive(self.signalPreamble() + dataBuffer)
