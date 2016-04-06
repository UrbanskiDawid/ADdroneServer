from time import gmtime, strftime
from datetime import datetime
import threading

class LogWriter:
    startEpoch = datetime(1970, 1, 1)
    logfile = None
    lock = None
    open = False

    def __init__(self):
        date = strftime("%d-%b-%Y-%H%M%S", gmtime())
        fileName = 'logs/ADDroneServer_' + date + '.log'
        self.logfile = open(fileName, 'w')
        self.lock = threading.Lock()
        self.open = True

    def millis(self):
        dt = datetime.now() - self.startEpoch
        ms = dt.microseconds / 1000.0
        return str(ms)

    def noteEvent(self, description):
        if self.open == False:
          return

        time = strftime("%H:%M:%S", gmtime())
        timeStamp = time + ":" + self.millis()
        self.lock.acquire()
        self.logfile.write(timeStamp + " " + description + "\n")
        self.lock.release()

    def close(self):
        self.logfile.close()
        self.open = False

