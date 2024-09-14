from time import time

class Timerizer:
    def __init__(self, max_time):
        """
        Inicializa um temporizador com um tempo máximo especificado

        Args:
            max_time (float): O tempo máximo para o temporizador em segundos
        """
        self.start_time = 0
        self.atual_time = 0
        self.is_run = False
        self.max_time = max_time

    def update(self):
        """
        Atualiza o temporizador, verificando se o tempo máximo foi alcançado
        Se o tempo máximo foi alcançado, o temporizador é desativado
        """
        self.atual_time = time()
        if self.atual_time - self.start_time >= self.max_time:
            self.is_run = False     

    def active(self):
        """
        Ativa o temporizador, definindo o tempo de início para o momento atual
        """
        self.is_run = True
        self.start_time = time()
    
    def deactive(self):
        self.is_run = False