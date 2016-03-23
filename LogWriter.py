from time import gmtime, strftime
from datetime import datetime


class LogWriter:
    startEpoch = datetime(1970, 1, 1)
    logfile = None

    def millis(self):
        dt = datetime.now() - self.startEpoch
        ms = dt.microseconds / 1000.0
        return str(ms)

    def __init__(self):
        date = strftime("%d-%b-%Y_%H-%M-%S", gmtime())
        fileName = 'logs/logs-' + date
        self.logfile = open(fileName, 'w')

    def noteEvent(self, description):
        time = strftime("%M:%S", gmtime())
        timeStamp = time + ":" + self.millis()
        self.logfile.write(timeStamp + " " + \
                           description + "\n")

    def closeFile(self):
        self.logfile.close()
