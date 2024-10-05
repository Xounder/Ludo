from typing import Callable, Optional

from managers.timer_manager import TimerManager

class Animation:
    """
    Represents an animation that can be executed based on a timer.
    """
    
    def __init__(self, timer_name:str, todo: Callable[[], None], callback: Optional[Callable[[], None]] = None) -> None:
        """
        Initializes an Animation instance.

        Args:
            timer_name (str): The name of the timer to control the animation.
            todo (Callable[[], None]): The function to be executed during the animation.
            callback (Optional[Callable[[], None]]): An optional function to call after the animation completes.
        """
        self.timer_name = timer_name
        self.todo = todo
        self.callback = callback
        self.is_animate = True

    def animate(self) -> bool:
        """
        Executes the animation if the timer is running.

        Returns:
            bool: True if the animation is still running, False if it has finished.
        """
        if TimerManager.is_run(self.timer_name):
            self.todo()
            return True
        else:
            if self.is_animate:
                self.is_animate = False
                if self.callback:
                    self.callback()
            return False