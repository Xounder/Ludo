import pygame
from managers.timer_manager import TimerManager

class InputManager:
    cursor = (0, 0)
    TimerManager.add_timer('mouse_timer', 0.4)

    @staticmethod
    def mouse_is_pressed():
        """
        Verifica se o botão esquerdo do mouse está pressionado e atualiza a posição do cursor

        Returns:
            bool: True se o botão esquerdo do mouse está pressionado, caso contrário, False
        """
        if TimerManager.is_run('mouse_timer'): return
        if pygame.mouse.get_pressed()[0]:
            InputManager.cursor = pygame.mouse.get_pos()
            TimerManager.active_timer('mouse_timer')
            return True
        return False