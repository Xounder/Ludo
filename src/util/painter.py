import pygame

class ClickRect: ####### Refatorar o Codigo do start-game adicionando aki
    def __init__(self) -> None:
        self.surf = None
        self.rect = None

    def draw_rect(self, size:list, pos:list, d:int, f_color='black', b_color='white') -> None:
        pygame.draw.rect(self.screen, f_color, (pos[0], pos[1], size[0], size[1]), 0)
        pygame.draw.rect(self.screen, b_color, (pos[0] + d , pos[1]+ d, size[0] - d*2 , size[1] - d*2), 0)

    def draw_animated_rect(self, size:list, pos:list, d:int, f_color='black'):
        b_c = 'red' if self.is_collide_point() else 'gray'
        self.draw_rect(size, pos, d, f_color=f_color, b_color=b_c)

    def is_collide_point(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())