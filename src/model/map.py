import pygame

import resource.settings as config

class Map:
    """
    Represents the game map and manages its rendering on the screen.
    """
    redraw_map = []

    def __init__(self) -> None:
        """
        Initializes the Map with a surface for rendering and copies the base map configuration.
        """
        self.screen = pygame.display.get_surface()
        self.map = config.ludo_map.copy()
        self.surf = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.line_y = pygame.Surface((2, config.TILE_SIZE))
        self.line_x = pygame.Surface((config.TILE_SIZE, 2))

    @staticmethod
    def add_redraw_map(redraw) -> None:
        """
        Adds a position to the redraw list for the map.

        Args:
            redraw: The position to be added for redrawing.
        """
        Map.redraw_map.append(redraw)

    def draw(self) -> None:
        """
        Draws the tiles that need to be redrawn based on the redraw list.
        """
        if Map.redraw_map:
            c = Map.redraw_map[0]
            self.blit_tile(c[0], c[1], self.map[c[1]][c[0]])
            Map.redraw_map.pop(0)
    
    def draw_map(self) -> None:
        """
        Draws the entire game map onto the screen.
        """
        for i, line in enumerate(self.map):
                for j, num in enumerate(line):
                    self.blit_tile(j, i, num)

    def blit_tile(self, j:int, i:int, num:int) -> None:
        """
        Renders a single tile on the screen at the specified coordinates.

        Args:
            j (int): The x-coordinate of the tile.
            i (int): The y-coordinate of the tile.
            num (int): The tile number used to determine the tile's color.
        """
        x = j * config.TILE_SIZE
        y = i * config.TILE_SIZE

        if num == -10:
                self.surf.fill('gray')
        elif config.star_steps.count(num):
                self.surf.fill('purple')
        else:
            color = ['yellow', 'blue', 'red', 'green']
            find = False
            for c in color:
                if config.check_color[c].count(num):
                    self.surf.fill(c)
                    find = True
                    break
            if not find:
                self.surf.fill('white')

        self.screen.blit(self.surf, (x, y))
        # black lines
        if 6 <= i <= 9:
            self.screen.blit(self.line_x, (x, y))
            if i != 9: self.screen.blit(self.line_y, (x, y))
        if 6 <= j <= 9:
            self.screen.blit(self.line_y, (x, y))
            if j != 9: self.screen.blit(self.line_x, (x, y))
