import pygame

class Painter:

    @staticmethod
    def blit_text(screen:pygame.display, text:str, color:str, pos:list, topright=False, center=False, font_size=42) -> None:
        font = pygame.font.Font('font/Pixeltype.ttf', font_size)
        txt = font.render(text, False, color)

        if topright: txt_rect = txt.get_rect(topright=(pos))
        elif center: txt_rect = txt.get_rect(center= (pos))
        else: txt_rect = txt.get_rect(topleft= (pos))       

        screen.blit(txt, txt_rect)

    @staticmethod
    def blit_text_shadow(screen:pygame.display, text:str, color:str, 
                         pos:list, back_color='black', topright=False, center=False, font_size=42) -> None:
        Painter.blit_text(screen, text, back_color, [pos[0] + 2, pos[1] + 2], topright, center, font_size)
        Painter.blit_text(screen, text, color, pos, topright, center, font_size)

    @staticmethod
    def draw_rect(screen:pygame.display, size:list, pos:list, d:int, f_color='black', b_color='white') -> None:
        pygame.draw.rect(screen, f_color, (pos[0], pos[1], size[0], size[1]), 0)
        pygame.draw.rect(screen, b_color, (pos[0] + d , pos[1]+ d, size[0] - d*2 , size[1] - d*2), 0)


class ClickRect:
    def __init__(self, surf_size:tuple, rect_pos:tuple, d=0, r=0, center=True, topleft=False) -> None:
        self.surf = pygame.Surface(surf_size)
        self.dist = d
        self.radius = r
        if center:
            self.rect = self.surf.get_rect(center=rect_pos)
        if topleft:
            self.rect = self.surf.get_rect(topleft=rect_pos)

    def draw_animated_rect(self, screen:pygame.display, f_color='black', b_color=['red', 'gray']):
        b_c = b_color[0] if self.is_rect_collide_point(pygame.mouse.get_pos()) else b_color[1]
        Painter.draw_rect(screen, self.rect.size, self.rect.topleft, self.dist, f_color=f_color, b_color=b_c)

    def draw_animated_circle(self, screen:pygame.display, colors:list):
        pygame.draw.circle(screen, colors[0], self.rect.center, self.radius, 3)
        pygame.draw.circle(screen, colors[1], self.rect.center, int(self.radius/2))
    
    def get_rect(self, center=False, topleft=False, size=False, midright=False):
        if center: return self.rect.center
        if topleft: return self.rect.topleft
        if size: return self.rect.size
        if midright: return self.rect.midright
        return self.rect
    
    def is_rect_collide_point(self, point:list):
        return self.rect.collidepoint(point)
    