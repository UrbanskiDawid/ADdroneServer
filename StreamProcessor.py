

class StreamProcessor:
    @staticmethod
    def controlPreamble():
        return '$$$$'

    @staticmethod
    def signalPreamble():
        return '%%%%'

    def getMaxBufferSize(self, preambleId):
        if (preambleId == self.controlPreamble()[0]):
            return 34
        elif (preambleId == self.signalPreamble()[0]):
            return 4
        else:
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

    def isPreamble(self, pream):
        a = (pream == self.controlPreamble())
        b = (pream == self.signalPreamble())
        return a or b

    def activatePreamble(self, preamValue):
        self.isPreambleActive = True
        self.activePreambleId = preamValue

    def putData(self, byte):
        self.dataBuffer += str(byte)
        if (len(self.dataBuffer) == self.getMaxBufferSize(self.activePreambleId)):
            # full packet according to preamble received
            self.onReceive();
            # cleanup for next reception
            self.isPreambleActive = False
            self.activePrembleId = None
            self.dataBuffer = ''

    # main method - called every data in stream is received
    def processStream(self, data):
        i = 0
        dataSize = len(data)
        while (i < dataSize):
            # check for preamble
            if (i + 4 < dataSize and self.isPreamble(data[i : i + 4])):
                self.activatePreamble(data[i])
                i += 4
                continue
            # else try to put byte into buffer if preable is received
            elif (self.isPreambleActive):
                self.putData(data[i])
            i += 1

    def onReceive(self):
        if (self.activePreambleId == self.controlPreamble()[0]):
            self.onControlReceive(self.controlPreamble() + self.dataBuffer)
        elif (self.activePreambleId == self.signalPreamble()[0]):
            self.onSignalReceive(self.signalPreamble() + self.dataBuffer)
