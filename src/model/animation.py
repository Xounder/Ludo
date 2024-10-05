from typing import Callable, Optional

from managers.timer_manager import TimerManager

class Animation:
    def __init__(self, timer_name:str, todo: Callable[[], None], callback: Optional[Callable[[], None]] = None) -> None:
        self.timer_name = timer_name
        self.todo = todo
        self.callback = callback
        self.is_animate = True

    def animate(self) -> bool:
        if TimerManager.is_run(self.timer_name):
            self.todo()
            return True
        else:
            if self.is_animate:
                self.is_animate = False
                if self.callback:
                    self.callback()
            return False