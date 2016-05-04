

class StreamProcessor:
    def controlPreamble():
        return '$$$$'

    def signalPreamble():
        return '%%%%'

    # handler for control packet receive event
    onControlReceive = None

    # handler for control packet receive event
    onSignalReceive = None

    # processing variables and containers


    def __init__(self, onControlReceive, onSignalReceive):
        self.onControlReceive = onControlReceive
        self.onSignalReceive = onSignalReceive

    # main method - called every data in stream is received
    def processStream(data):
        i = 0
        dataSize = len(data)
        while i < dataSize:
            i += 1
