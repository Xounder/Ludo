import pygame
import resource.settings as config

class Map:
    redraw_map = []

    def __init__(self) -> None:
        """
        Inicializa o mapa com a tela de exibição, a configuração do mapa e os objetos de superfície 
        para desenho dos tiles e linhas
        """
        self.screen = pygame.display.get_surface()
        self.map = config.ludo_map.copy()
        self.surf = pygame.Surface((config.TILE_SIZE, config.TILE_SIZE))
        self.line_y = pygame.Surface((2, config.TILE_SIZE))
        self.line_x = pygame.Surface((config.TILE_SIZE, 2))

    @staticmethod
    def add_redraw_map(redraw):
        """
        Adiciona uma nova posição de tile à lista de tiles a serem redesenhados

        Args:
            redraw (tuple): Coordenadas do tile a ser redesenhado
        """
        Map.redraw_map.append(redraw)

    def draw(self) -> None:
        """
        Desenha os tiles que precisam ser redesenhados, conforme listado em `Map.redraw_map`
        """
        if Map.redraw_map:
            c = Map.redraw_map[0]
            self.blit_tile(c[0], c[1], self.map[c[1]][c[0]])
            Map.redraw_map.pop(0)
    
    def draw_map(self) -> None:
        """
        Desenha todo o mapa na tela
        """
        for i, line in enumerate(self.map):
                for j, num in enumerate(line):
                    self.blit_tile(j, i, num)

    def blit_tile(self, j:int, i:int, num:int) -> None:
        """
        Desenha um tile com a cor da posição indicada

        Args:
            j (int): Coordenada x do tile
            i (int): Coordenada y do tile
            num (int): Número que determina a cor do tile
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
