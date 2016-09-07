

class StreamProcessor:
    @staticmethod
    def controlPreamble():
        return '$$$$'

    @staticmethod
    def signalPreamble():
        return '%%%%'

    @staticmethod
    def autopilotPreamble():
        return '^^^^'

    def getMaxBufferSize(self, preambleId):
        if preambleId == self.controlPreamble()[0]:
            return 34
        elif preambleId == self.signalPreamble()[0]:
            return 6
        elif preambleId == self.autopilotPreamble()[0]:
            return 26
        else:
            print 'Bad preamble Id'
            raise 

    # handler for control packet receive event
    # argument - string of received data WITH preamble
    onControlReceive = None

    # handler for signal(ping) packet receive event
    # argument - string of received data WITH preamble
    onSignalReceive = None

    # handler for autopilot packet receive event
    # argument - string of received data WITH preamble
    onAutopilotReceive = None

    # processing variables and containers
    isPreambleActive = False
    activePreambleId = None

    dataBuffer = ''

    def __init__(self, onControlReceive, onSignalReceive, onAutopilotReceive):
        self.onControlReceive = onControlReceive
        self.onSignalReceive = onSignalReceive
        self.onAutopilotReceive = onAutopilotReceive
        self.activePreambleId = None

    def isPreamble(self, pream):
        control = (pream == self.controlPreamble())
        signal = (pream == self.signalPreamble())
        auto = (pream == self.autopilotPreamble())
        return control or signal or auto

    def activatePreamble(self, preamValue):
        self.isPreambleActive = True
        self.activePreambleId = preamValue

    def putData(self, byte):
        self.dataBuffer += str(byte)
        if len(self.dataBuffer) == self.getMaxBufferSize(self.activePreambleId):
            # full packet according to preamble received
            self.onReceive()
            # cleanup for next reception
            self.isPreambleActive = False
            self.activePreambleId = None
            self.dataBuffer = ''

    # main method - called every data in stream is received
    def processStream(self, data):
        i = 0
        dataSize = len(data)
        while i < dataSize:
            # check for preamble
            if i + 4 < dataSize and self.isPreamble(data[i : i + 4]):
                self.activatePreamble(data[i])
                i += 4
                continue
            # else try to put byte into buffer if preable is received
            elif self.isPreambleActive:
                self.putData(data[i])
            i += 1

    def onReceive(self):
        if self.activePreambleId == self.controlPreamble()[0]:
            self.onControlReceive(self.controlPreamble() + self.dataBuffer)
        elif self.activePreambleId == self.signalPreamble()[0]:
            self.onSignalReceive(self.signalPreamble() + self.dataBuffer)
        elif self.activePreambleId == self.autopilotPreamble()[0]:
            self.onAutopilotReceive(self.autopilotPreamble() + self.dataBuffer)
