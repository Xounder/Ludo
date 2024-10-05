from typing import Callable, Optional

from model.animation import Animation
from managers.timer_manager import TimerManager

class UpdaterManager:
    update_list = {}
    current_animate = None
    exclusive_update = None
    exclusive_callback = None
    is_exclusive_callback = False

    @staticmethod
    def add_to_update_list(to_update:Callable[[], None]) -> None:
        UpdaterManager.update_list[to_update] = to_update

    @staticmethod
    def set_exclusive_update(to_update:object, callback: Optional[Callable[[], None]] = None):
        if UpdaterManager.exclusive_update == to_update: return
        UpdaterManager.exclusive_update = to_update
        UpdaterManager.exclusive_callback = callback
        UpdaterManager.is_exclusive_callback = True if callback else False
        
    @staticmethod
    def stop_exclusive_update():
        UpdaterManager.exclusive_update = None
        UpdaterManager.exclusive_callback = None
        UpdaterManager.is_exclusive_callback = False

    @staticmethod
    def add_to_animate(timer_name:str, duration:int) -> None:
        TimerManager.add_timer(timer_name, duration)

    @staticmethod
    def finish_animation(timer_name:str) -> None:
        TimerManager.deactive(timer_name)

    @staticmethod
    def call_to_animate(timer_name:str, todo:Callable[[], None], callback: Optional[Callable[[], None]] = None) -> None:
        TimerManager.active_timer(timer_name)
        UpdaterManager.current_animate = Animation(timer_name, todo, callback)
        
    @staticmethod
    def update() -> None:
        TimerManager.update_timers()
        if UpdaterManager.current_animate and UpdaterManager.current_animate.animate(): return
        if UpdaterManager.is_exclusive_update(): return
        if not UpdaterManager.update_list: return
        for update in UpdaterManager.update_list:
            update()
        
    def is_exclusive_update() -> None:
        if UpdaterManager.exclusive_update:
            UpdaterManager.exclusive_update.update()
            if not UpdaterManager.exclusive_update.active and UpdaterManager.is_exclusive_callback:
                UpdaterManager.is_exclusive_callback = False
                UpdaterManager.exclusive_callback()
            return True
        return False
