from threading import Thread
import time
import sys
import gphoto2 as gp

class Countdown():
    def __init__(self, stepsManager, duration, endFunction):
        self.stepsManager = stepsManager
        self.endFunction = endFunction
        self.duration = duration
        self.counter = self.duration
        self.isStarted = False
        self.thread = Thread(target=self.count)
        
    def start(self):
        self.isStarted = True
        self.counter = self.duration
        self.thread.start()
    
    def count(self):
        for i in range(self.duration):
            self.counter = self.duration-i
            time.sleep(1)
        if gp.Camera.autodetect():
            self.stepsManager.step = self.endFunction
        self.isStarted = False
        sys.exit()
