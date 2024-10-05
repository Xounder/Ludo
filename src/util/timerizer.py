from time import time

class Timerizer:
    """
    Manages a timer that can be activated and checked for expiration.
    """

    def __init__(self, max_time:float) -> None:
        """
        Initializes the timer with a maximum time limit.
        
        Args:
            max_time (float): The maximum duration of the timer in seconds.
        """
        self.start_time = 0
        self.atual_time = 0
        self.is_run = False
        self.max_time = max_time

    def update(self) -> None:
        """
        Updates the current time and checks if the timer has expired.
        If the timer has expired, it sets is_run to False.
        """
        self.atual_time = time()
        if self.atual_time - self.start_time >= self.max_time:
            self.is_run = False     

    def active(self) -> None:
        """
        Activates the timer, recording the current time as the start time.
        """
        self.is_run = True
        self.start_time = time()
    
    def deactive(self) -> None:
        """
        Deactivates the timer, setting is_run to False.
        """
        self.is_run = False