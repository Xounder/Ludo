from util.timerizer import Timerizer

class TimerManager:
    timers = {}

    @staticmethod
    def add_timer(timer_name:str, duration:float) -> None:
        TimerManager.timers[timer_name] = Timerizer(duration)

    @staticmethod
    def update_timers() -> None:
        for t_name, t_obj in TimerManager.timers.items():
            if t_obj.is_run:
                t_obj.update()
    
    @staticmethod
    def active_timer(timer_name:str) -> None:
        if timer_name in TimerManager.timers:
            TimerManager.timers[timer_name].active()
        else:
            print(f'Timer {timer_name} não encontrado.')

    @staticmethod
    def is_run(timer_name:str) -> bool:
        if timer_name in TimerManager.timers:
            return TimerManager.timers[timer_name].is_run
        else:
            print(f'Timer {timer_name} não encontrado.')
            return False
        
    @staticmethod
    def deactive(timer_name:str) -> None:
        TimerManager.timers[timer_name].deactive()