import pygame
from util.timer_management import TimerManagement

class InputManagement:
    cursor = (0, 0)
    TimerManagement.add_timer('mouse_timer', 0.4)

    @staticmethod
    def mouse_is_pressed():
        """
        Verifica se o botão esquerdo do mouse está pressionado e atualiza a posição do cursor
        Utiliza um temporizador para evitar verificações excessivas

        Returns:
            bool: Retorna True se o botão esquerdo do mouse está pressionado, caso contrário, False
        """
        if TimerManagement.is_run('mouse_timer'): return
        if pygame.mouse.get_pressed()[0]:
            InputManagement.cursor = pygame.mouse.get_pos()
            TimerManagement.active_timer('mouse_timer')
            return True
        return False