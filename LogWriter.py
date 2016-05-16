from datetime import datetime
import threading

class LogWriter:
    startEpoch = datetime(1970, 1, 1)
    logfile = None
    lock = None
    open = False

    def __init__(self,dir):
        date = datetime.now().strftime('%d-%b-%Y_%H%M%S')
        fileName = dir+'/ADDroneServer_' + date + '.log'
        print("LogWriter: starting '"+fileName+"'");
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

        time = datetime.now().strftime('%H:%M:%S')
        timeStamp = time + ":" + self.millis()
        self.lock.acquire()
        self.logfile.write(timeStamp + " " + description + "\n")
        self.lock.release()

    def close(self):
        self.logfile.close()
        self.open = False

