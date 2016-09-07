from ControlData import *
from threading import Thread, Event, Lock
import time

class TimerThread(Thread):
    def __init__(self, Name, handler, interval):
        Thread.__init__(self)
        self.name = Name
        self.stopped = Event()
        self.handler = handler
        self.interval = interval

    def run(self):
        while not self.stopped.wait(self.interval):
            if self.stopped.isSet():
                #print "TimerThread: Breaking ",self.name,"thread."
                break
            self.handler()

    def stop(self):
        print "TimerThread: stopping ",self.name
        self.stopped.set()

    @staticmethod
    def kill(timerThread):
      if timerThread is None:
        return
      timerThread.stop()
      timerThread.join()
      timerThread = None
      
