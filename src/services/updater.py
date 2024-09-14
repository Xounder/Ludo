from typing import Callable, Optional

from util.timer_management import TimerManagement
from model.animation import Animation

class Updater:
    update_list = {}
    current_animate = None
    exclusive_update = None
    exclusive_callback = None
    is_exclusive_callback = False

    @staticmethod
    def add_to_update_list(to_update:Callable[[], None]) -> None:
        Updater.update_list[to_update] = to_update

    @staticmethod
    def set_exclusive_update(to_update:object, callback: Optional[Callable[[], None]] = None):
        if Updater.exclusive_update == to_update: return
        Updater.exclusive_update = to_update
        Updater.exclusive_callback = callback
        Updater.is_exclusive_callback = True if callback else False
        
    @staticmethod
    def stop_exclusive_update():
        Updater.exclusive_update = None

    @staticmethod
    def add_to_animate(timer_name:str, duration:int) -> None:
        TimerManagement.add_timer(timer_name, duration)

    @staticmethod
    def call_to_animate(timer_name:str, todo:Callable[[], None], callback: Optional[Callable[[], None]] = None) -> None:
        TimerManagement.active_timer(timer_name)
        Updater.current_animate = Animation(timer_name, todo, callback)
        
    @staticmethod
    def update() -> None:
        TimerManagement.update_timers()
        if Updater.current_animate and Updater.current_animate.animate(): return
        if Updater.is_exclusive_update(): return
        if not Updater.update_list: return
        for update in Updater.update_list:
            update()
        
    def is_exclusive_update() -> None:
        if Updater.exclusive_update:
            Updater.exclusive_update.update()
            if not Updater.exclusive_update.active and Updater.is_exclusive_callback:
                Updater.is_exclusive_callback = False
                Updater.exclusive_callback()
            return True
        return False
