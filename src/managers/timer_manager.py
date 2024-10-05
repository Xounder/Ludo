from util.timerizer import Timerizer

class TimerManager:
    """
    Manages timers for tracking durations and updates.
    """
    timers = {}

    @staticmethod
    def add_timer(timer_name:str, duration:float) -> None:
        """
        Adds a new timer to the TimerManager.

        Args:
            timer_name (str): The name of the timer.
            duration (float): The duration of the timer in seconds.
        """
        TimerManager.timers[timer_name] = Timerizer(duration)

    @staticmethod
    def update_timers() -> None:
        """
        Updates all active timers.
        """
        for t_name, t_obj in TimerManager.timers.items():
            if t_obj.is_run:
                t_obj.update()
    
    @staticmethod
    def active_timer(timer_name:str) -> None:
        """
        Checks if the specified timer is running.

        Args:
            timer_name (str): The name of the timer to check.

        Returns:
            bool: True if the timer is running, False otherwise.
        """
        if timer_name in TimerManager.timers:
            TimerManager.timers[timer_name].active()
        else:
            print(f'Timer {timer_name} não encontrado.')

    @staticmethod
    def is_run(timer_name:str) -> bool:
        """
        Checks if the specified timer is running.

        Args:
            timer_name (str): The name of the timer to check.

        Returns:
            bool: True if the timer is running, False otherwise.
        """
        if timer_name in TimerManager.timers:
            return TimerManager.timers[timer_name].is_run
        else:
            print(f'Timer {timer_name} não encontrado.')
            return False
        
    @staticmethod
    def deactive(timer_name:str) -> None:
        """
        Deactivates the specified timer.

        Args:
            timer_name (str): The name of the timer to deactivate.
        """
        TimerManager.timers[timer_name].deactive()