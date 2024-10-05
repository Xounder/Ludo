from typing import Callable, Optional

from model.animation import Animation
from managers.timer_manager import TimerManager

class UpdaterManager:
    """
    Manages updates for animation and other callable tasks.
    """
    update_list = {}
    current_animate = None
    exclusive_update = None
    exclusive_callback = None
    is_exclusive_callback = False

    @staticmethod
    def add_to_update_list(to_update:Callable[[], None]) -> None:
        """
        Adds a callable to the update list.

        Args:
            to_update (Callable[[], None]): The callable to add to the update list.
        """
        UpdaterManager.update_list[to_update] = to_update

    @staticmethod
    def set_exclusive_update(to_update:object, callback: Optional[Callable[[], None]] = None) -> None:
        """
        Sets an exclusive update task.

        Args:
            to_update (object): The task to set as exclusive.
            callback (Optional[Callable[[], None]]): Optional callback to execute after the exclusive update.
        """
        if UpdaterManager.exclusive_update == to_update: return
        UpdaterManager.exclusive_update = to_update
        UpdaterManager.exclusive_callback = callback
        UpdaterManager.is_exclusive_callback = True if callback else False
        
    @staticmethod
    def stop_exclusive_update() -> None:
        """
        Stops the current exclusive update task.
        """
        UpdaterManager.exclusive_update = None
        UpdaterManager.exclusive_callback = None
        UpdaterManager.is_exclusive_callback = False

    @staticmethod
    def add_to_animate(timer_name:str, duration:int) -> None:
        """
        Adds a timer for animation.

        Args:
            timer_name (str): The name of the timer.
            duration (int): The duration of the timer in seconds.
        """
        TimerManager.add_timer(timer_name, duration)

    @staticmethod
    def finish_animation(timer_name:str) -> None:
        """
        Finishes the specified animation by deactivating its timer.

        Args:
            timer_name (str): The name of the timer associated with the animation.
        """
        TimerManager.deactive(timer_name)

    @staticmethod
    def call_to_animate(timer_name:str, todo:Callable[[], None], callback: Optional[Callable[[], None]] = None) -> None:
        """
        Calls the animation function associated with the timer.

        Args:
            timer_name (str): The name of the timer.
            todo (Callable[[], None]): The animation function to call.
            callback (Optional[Callable[[], None]]): Optional callback to execute after the animation.
        """
        TimerManager.active_timer(timer_name)
        UpdaterManager.current_animate = Animation(timer_name, todo, callback)
        
    @staticmethod
    def update() -> None:
        """
        Updates all active timers and calls the appropriate update functions.
        """
        TimerManager.update_timers()
        if UpdaterManager.current_animate and UpdaterManager.current_animate.animate(): return
        if UpdaterManager.is_exclusive_update(): return
        if not UpdaterManager.update_list: return
        for update in UpdaterManager.update_list:
            update()
        
    def is_exclusive_update() -> None:
        """
        Checks if an exclusive update is active and executes it.

        Returns:
            bool: True if an exclusive update is active, False otherwise.
        """
        if UpdaterManager.exclusive_update:
            UpdaterManager.exclusive_update.update()
            if not UpdaterManager.exclusive_update.active and UpdaterManager.is_exclusive_callback:
                UpdaterManager.is_exclusive_callback = False
                UpdaterManager.exclusive_callback()
            return True
        return False
