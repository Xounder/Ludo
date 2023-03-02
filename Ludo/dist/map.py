map = [[-3,  -3,  -3,  -3,  -3,  -3,  37,  38,  39,  -4,  -4,  -4,  -4,  -4, -4],
       [-3,   0,   0,   0,   0,  -3,  36, 401,  40,  -4,   0,   0,   0,   0, -4],
       [-3,   0,   0,   0,   0,  -3,  35, 402,  41,  -4,   0,   0,   0,   0, -4],
       [-3,   0,   0,   0,   0,  -3,  34, 403,  42,  -4,   0,   0,   0,   0, -4],
       [-3,   0,   0,   0,   0,  -3,  33, 404,  43,  -4,   0,   0,   0,   0, -4],
       [-3,  -3,  -3,  -3,  -3,  -3,  32, 405,  44,  -4,  -4,  -4,  -4,  -4, -4],
       [26,  27,  28,  29,  30,  31, -10, 406, -10,  45,  46,  47,  48,  49, 50],
       [25, 301, 302, 303, 304, 305, 306, -10, 106, 105, 104, 103, 102, 101, 51],
       [24,  23,  22,  21,  20,  19, -10, 206, -10,   5,   4,   3,   2,   1, 52],
       [-2,  -2,  -2,  -2,  -2,  -2,  18, 205,   6,  -1,  -1,  -1,  -1,  -1, -1],
       [-2,   0,   0,   0,   0,  -2,  17, 204,   7,  -1,   0,   0,   0,   0, -1],
       [-2,   0,   0,   0,   0,  -2,  16, 203,   8,  -1,   0,   0,   0,   0, -1],
       [-2,   0,   0,   0,   0,  -2,  15, 202,   9,  -1,   0,   0,   0,   0, -1],
       [-2,   0,   0,   0,   0,  -2,  14, 201,   10, -1,   0,   0,   0,   0, -1],
       [-2,  -2,  -2,  -2,  -2,  -2,  13,  12,   11, -1,  -1,  -1,  -1,  -1, -1]]

import pygame
from settings import tile_size, star_cells

class Map:
       def __init__(self):
              self.display_surface = pygame.display.get_surface()
              self.map = map
              self.surf = pygame.Surface((tile_size, tile_size))
              self.line_y = pygame.Surface((2, tile_size))
              self.line_x = pygame.Surface((tile_size, 2))

       def draw(self):
              for j, col in enumerate(map):
                     for i, num in enumerate(col):
                            x = i * tile_size
                            y = j * tile_size
                            if num == -1 or 101 <= num <= 106 or num == 1:
                                   self.surf.fill('yellow')
                            elif num == -2 or 201 <= num <= 206 or num == 14:
                                   self.surf.fill('blue')
                            elif num == -3 or 301 <= num <= 306 or num == 27:
                                   self.surf.fill('red')
                            elif num == -4 or 401 <= num <= 406 or num == 40:
                                   self.surf.fill('green')
                            elif num == -10:
                                   self.surf.fill('gray')
                            elif num == star_cells[0] or num == star_cells[1] or num == star_cells[2] or num == star_cells[3]:
                                   self.surf.fill('purple')
                            else:
                                   self.surf.fill('white')

                            self.display_surface.blit(self.surf, (x, y))
                            # black lines
                            if (((0 <= j < 6 or 9 <= j < 15) and 6 <= i <= 9) or 6 <= j <= 8 or i == 0 
                                                               or ((i == 1 or i == 5 or i == 10 or i == 14) and (0 < j < 5 or 9 < j < 14))):
                                   self.display_surface.blit(self.line_y, (x, y))
                            if (((0 <= j < 6 or 9 <= j < 15) and 6 <= i < 9) or 6 <= j <= 9 or j == 0 
                                                               or ((j == 1 or j == 5 or j == 10 or j == 14) and (0 < i < 5 or 9 < i < 14))):
                                   self.display_surface.blit(self.line_x, (x, y))

