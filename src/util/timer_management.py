from util.timerizer import Timerizer

class TimerManagement:
    timers = {}

    @staticmethod
    def add_timer(timer_name:str, duration:float) -> None:
        """
        Adiciona um novo temporizador à lista de temporizadores gerenciados

        Args:
            timer_name (str): O nome do temporizador
            duration (float): A duração do temporizador em segundos
        """
        TimerManagement.timers[timer_name] = Timerizer(duration)

    @staticmethod
    def update_timers() -> None:
        """
        Atualiza todos os temporizadores gerenciados que estão em execução
        """
        for t_name, t_obj in TimerManagement.timers.items():
            if t_obj.is_run:
                t_obj.update()
    
    @staticmethod
    def active_timer(timer_name:str) -> None:
        """
        Ativa um temporizador existente, fazendo com que ele comece a contar o tempo

        Args:
            timer_name (str): O nome do temporizador a ser ativado

        Raises:
            ValueError: Se o nome do temporizador não estiver presente na lista de temporizadores
        """
        if timer_name in TimerManagement.timers:
            TimerManagement.timers[timer_name].active()
        else:
            print(f'Timer {timer_name} não encontrado.')

    @staticmethod
    def is_run(timer_name:str) -> bool:
        """
        Verifica se um temporizador específico está em execução

        Args:
            timer_name (str): O nome do temporizador a ser verificado

        Returns:
            bool: Retorna True se o temporizador está em execução, caso contrário, False

        Raises:
            ValueError: Se o nome do temporizador não estiver presente na lista de temporizadores
        """
        if timer_name in TimerManagement.timers:
            return TimerManagement.timers[timer_name].is_run
        else:
            print(f'Timer {timer_name} não encontrado.')
            return False
        
    @staticmethod
    def deactive(timer_name:str) -> None:
        TimerManagement.timers[timer_name].deactive()