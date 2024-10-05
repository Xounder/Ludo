import pygame

class Painter:
    """
    Provides static methods for drawing text and rectangles on the screen.
    """

    @staticmethod
    def blit_text(screen:pygame.display, text:str, color:str, pos:list, 
                  topright:bool=False, center:bool=False, font_size:int=42) -> None:
        """
        Renders and blits text onto the screen at the specified position.
        
        Args:
            screen (pygame.display): The surface to draw on.
            text (str): The text to render.
            color (str): The color of the text.
            pos (list): The position to place the text.
            topright (bool): If True, position text at the top right corner.
            center (bool): If True, center the text at the given position.
            font_size (int): The font size for the text.
        """
        font = pygame.font.Font('font/Pixeltype.ttf', font_size)
        txt = font.render(text, False, color)

        if topright: txt_rect = txt.get_rect(topright=(pos))
        elif center: txt_rect = txt.get_rect(center= (pos))
        else: txt_rect = txt.get_rect(topleft= (pos))       

        screen.blit(txt, txt_rect)

    @staticmethod
    def blit_text_shadow(screen:pygame.display, text:str, color:str, pos:list, 
                         back_color:str='black', topright:bool=False, center:bool=False, font_size:int=42) -> None:
        """
        Renders and blits text with a shadow effect on the screen.
        
        Args:
            screen (pygame.display): The surface to draw on.
            text (str): The text to render.
            color (str): The color of the text.
            pos (list): The position to place the text.
            back_color (str): The color of the shadow.
            topright (bool): If True, position text at the top right corner.
            center (bool): If True, center the text at the given position.
            font_size (int): The font size for the text.
        """
        Painter.blit_text(screen, text, back_color, [pos[0] + 2, pos[1] + 2], topright, center, font_size)
        Painter.blit_text(screen, text, color, pos, topright, center, font_size)

    @staticmethod
    def draw_rect(screen:pygame.display, size:list, pos:list, d:int, f_color:str='black', b_color:str='white') -> None:
        """
        Draws a filled rectangle with a border on the screen.
        
        Args:
            screen (pygame.display): The surface to draw on.
            size (list): The size of the rectangle.
            pos (list): The position to draw the rectangle.
            d (int): The border thickness.
            f_color (str): The fill color of the rectangle.
            b_color (str): The border color of the rectangle.
        """
        pygame.draw.rect(screen, f_color, (pos[0], pos[1], size[0], size[1]), 0)
        pygame.draw.rect(screen, b_color, (pos[0] + d , pos[1]+ d, size[0] - d*2 , size[1] - d*2), 0)


class ClickRect:
    """
    Represents a clickable rectangle with optional animation effects.
    """

    def __init__(self, surf_size:tuple, rect_pos:tuple, d:int=0, r:int=0, center:bool=True, topleft:bool=False) -> None:
        """
        Initializes the clickable rectangle with given dimensions and position.
        
        Args:
            surf_size (tuple): The size of the rectangle surface.
            rect_pos (tuple): The position to draw the rectangle.
            d (int): The distance for border thickness.
            r (int): The radius for circle effects.
            center (bool): If True, position the rectangle centered at rect_pos.
            topleft (bool): If True, position the rectangle at the top-left of rect_pos.
        """
        self.surf = pygame.Surface(surf_size)
        self.dist = d
        self.radius = r
        if center:
            self.rect = self.surf.get_rect(center=rect_pos)
        if topleft:
            self.rect = self.surf.get_rect(topleft=rect_pos)

    def draw_animated_rect(self, screen:pygame.display, f_color:str='black', b_color:list=['red', 'gray']) -> None:
        """
        Draws an animated rectangle with color changes based on mouse hover.
        
        Args:
            screen (pygame.display): The surface to draw on.
            f_color (str): The fill color of the rectangle.
            b_color (list): The background colors for hover effects.
        """
        b_c = b_color[0] if self.is_rect_collide_point(pygame.mouse.get_pos()) else b_color[1]
        Painter.draw_rect(screen, self.rect.size, self.rect.topleft, self.dist, f_color=f_color, b_color=b_c)

    def draw_animated_circle(self, screen:pygame.display, colors:list) -> None:
        """
        Draws animated circles with specified colors at the rectangle's center.
        
        Args:
            screen (pygame.display): The surface to draw on.
            colors (list): A list of colors for the circles.
        """
        pygame.draw.circle(screen, colors[0], self.rect.center, self.radius, 3)
        pygame.draw.circle(screen, colors[1], self.rect.center, int(self.radius/2))
    
    def get_rect(self, center:bool=False, topleft:bool=False, size:bool=False, midright:bool=False) -> pygame.Rect:
        """
        Returns the rectangle's position or size based on specified flags.
        
        Args:
            center (bool): If True, return the center of the rectangle.
            topleft (bool): If True, return the top-left position of the rectangle.
            size (bool): If True, return the size of the rectangle.
            midright (bool): If True, return the mid-right position of the rectangle.
        
        Returns:
            pygame.Rect: The rectangle's position or size based on flags.
        """
        if center: return self.rect.center
        if topleft: return self.rect.topleft
        if size: return self.rect.size
        if midright: return self.rect.midright
        return self.rect
    
    def is_rect_collide_point(self, point:list) -> bool:
        """
        Checks if the given point collides with the rectangle.
        
        Args:
            point (list): The point to check for collision.
        
        Returns:
            bool: True if the point collides with the rectangle, False otherwise.
        """
        return self.rect.collidepoint(point)
    