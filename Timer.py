import time

class Timer():
    def __init__(self, offset = 0):
        self.start = time.time() - offset

    def elapsed(self):
        return time.time() - self.start