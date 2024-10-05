import pygame
from managers.timer_manager import TimerManager

class InputManager:
    """
    Manages mouse input and cursor position.
    """
    cursor = (0, 0)
    TimerManager.add_timer('mouse_timer', 0.4)

    @staticmethod
    def mouse_is_pressed() -> bool:
        """
        Checks if the left mouse button is pressed.

        Returns:
            bool: True if the left mouse button is pressed, False otherwise.
        """
        if TimerManager.is_run('mouse_timer'): return
        if pygame.mouse.get_pressed()[0]:
            InputManager.cursor = pygame.mouse.get_pos()
            TimerManager.active_timer('mouse_timer')
            return True
        return False