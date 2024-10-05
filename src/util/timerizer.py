from time import time

class Timerizer:
    def __init__(self, max_time):
        self.start_time = 0
        self.atual_time = 0
        self.is_run = False
        self.max_time = max_time

    def update(self):
        self.atual_time = time()
        if self.atual_time - self.start_time >= self.max_time:
            self.is_run = False     

    def active(self):
        self.is_run = True
        self.start_time = time()
    
    def deactive(self):
        self.is_run = False