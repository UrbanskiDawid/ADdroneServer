from time import gmtime, strftime
from datetime import datetime
import threading

class LogWriter:
    startEpoch = datetime(1970, 1, 1)
    logfile = None
    lock = None

    def __init__(self):
        date = strftime("%d-%b-%Y-%H%M%S", gmtime())
        fileName = 'logs-'.rstrip() + date
        self.logfile = open(fileName, 'w')
        self.lock = threading.Lock

    def millis(self):
        dt = datetime.now() - self.startEpoch
        ms = dt.microseconds / 1000.0
        return str(ms)


    def noteEvent(self, description):
        time = strftime("%M:%S", gmtime())
        timeStamp = time + ":" + self.millis()
        self.lock.acquire()
        self.logfile.write(timeStamp + " " + \
                           description + "\n")
        self.lock.release()

    def closeFile(self):
        self.logfile.close()
