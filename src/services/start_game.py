import pygame

from util.input_management import InputManagement

import resource.settings as config

class StartGame:
    def __init__(self) -> None:
        """
        Inicializa a tela de início do jogo, configurando a posição e o tamanho dos elementos 
        e criando superfícies para os botões e seletores
        """
        self.screen = pygame.display.get_surface()
        self.size = (300, 260)
        self.pos = (config.SCREEN_WIDTH/2 - self.size[0]/2, config.SCREEN_HEIGHT/2 - self.size[1]/2)
        
        self.init()
        self.create_surf_inputs()

    def init(self) -> None:
        """
        Inicializa as variáveis da tela de início, incluindo os seletores de cor e jogador
        """
        self.players = []
        self.active = True
        self.active_game_controller = True
        self.selectors = [
            {'color': 0, 'player': config.PLAYER},
            {'color': 1, 'player': config.PLAYER},
            {'color': 2, 'player': config.PLAYER},
            {'color': 3, 'player': config.PLAYER}
        ]

    def create_surf_inputs(self) -> None:
        """
        Cria superfícies para os botões de início, seleção de cor e seleção de jogador
        """
        # Start Button
        self.start_button = pygame.Surface((90, 60))
        self.start_button_rect = self.start_button.get_rect(topleft=((config.SCREEN_WIDTH/2 + 40, config.SCREEN_HEIGHT/2 - 15)))
        # Color Selection Button
        self.color_selection = []
        # Player Selection Button
        self.player_selection = []
        pos = [40, 95]
        for i in range(4):
            # Color
            surf = pygame.Surface((20, 20))
            rect = surf.get_rect(center=(self.pos[0] + pos[0], self.pos[1] + pos[1]))
            self.color_selection.append({'surface': surf, 'rect': rect})
            # Player
            surf = pygame.Surface((100, 30))
            rect = surf.get_rect(topleft=(self.pos[0] + pos[0] + 20, self.pos[1] + pos[1] - 15))
            self.player_selection.append({'surface': surf, 'rect': rect})

            pos[1] += 40

    def draw(self) -> None:
        """
        Desenha a tela de início, incluindo botões e seletores de cor e jogador
        """
        d = 10
        self.draw_rect(self.size, self.pos, d)

        f_c = 'black' if self.is_start_game() else 'red'
        self.draw_animated_rect(self.start_button_rect, self.start_button_rect.size, 
                                self.start_button_rect.topleft, 3, f_color=f_c)
            
        for i in range(4):
            self.draw_selector(i)

    def draw_selector(self, id:int) -> None:
        """
        Desenha o seletor de cor e jogador para um índice específico

        Args:
            id (int): O índice do seletor a ser desenhado
        """
        atual_sel = self.selectors[id]
        c = (['gray', 'gray'] if atual_sel['player'] == config.INACTIVE 
                             else ['black', config.colors[atual_sel['color']]])
        button_color = self.color_selection[id]
        button_player = self.player_selection[id]

        pygame.draw.circle(self.screen, c[0], button_color['rect'].center, 10, 3)
        pygame.draw.circle(self.screen, c[1], button_color['rect'].center, 5)
        self.draw_animated_rect(button_player['rect'], button_player['rect'].size, 
                                button_player['rect'].topleft, 2, f_color='black')

    def draw_rect(self, size:list, pos:list, d:int, f_color='black', b_color='white') -> None:
        """
        Desenha um retângulo com uma borda

        Args:
            size (list): O tamanho do retângulo [largura, altura]
            pos (list): A posição do retângulo [x, y]
            d (int): A espessura da borda
            f_color (str, opcional): A cor de preenchimento do retângulo. Padrão é 'black'
            b_color (str, opcional): A cor da borda do retângulo. Padrão é 'white'
        """
        pygame.draw.rect(self.screen, f_color, (pos[0], pos[1], size[0], size[1]), 0)
        pygame.draw.rect(self.screen, b_color, (pos[0] + d , pos[1]+ d, size[0] - d*2 , size[1] - d*2), 0)

    def draw_animated_rect(self, rect:pygame.rect.Rect, size:list, pos:list, d:int, f_color='black'):
        """
        Desenha um retângulo que muda de cor quando o cursor está sobre ele

        Args:
            rect (pygame.rect.Rect): O retângulo a ser desenhado
            size (list): O tamanho do retângulo [largura, altura]
            pos (list): A posição do retângulo [x, y]
            d (int): A espessura da borda
            f_color (str, opcional): A cor de preenchimento do retângulo. Padrão é 'black'
        """
        b_c = 'red' if rect.collidepoint(pygame.mouse.get_pos()) else 'gray'
        self.draw_rect(size, pos, d, f_color=f_color, b_color=b_c)

    def update(self) -> None:
        """
        Atualiza a tela de início, verificando a interação do usuário com os botões e seletores
        """
        if InputManagement.mouse_is_pressed():
            if self.start_button_rect.collidepoint(InputManagement.cursor):
                self.active = not self.is_start_game()
            else:
                for i, b_color in enumerate(self.color_selection):
                    if self.selectors[i]['player'] == config.INACTIVE: continue
                    if b_color['rect'].collidepoint(InputManagement.cursor):
                        self.selectors[i]['color'] = (self.selectors[i]['color'] + 1) % len(config.colors)
                        return

                for i, ply_sel in enumerate(self.player_selection):
                    if ply_sel['rect'].collidepoint(InputManagement.cursor):
                        self.selectors[i]['player'] = (self.selectors[i]['player'] + 1) % 3
                        break
            
    def is_start_game(self) -> bool:
        """
        Verifica se o jogo pode começar, ou seja, se todos os jogadores selecionados têm cores únicas

        Returns:
            bool: Retorna True se o jogo pode começar, caso contrário, False
        """
        check = []
        for sel in self.selectors:
            if sel['player'] == config.INACTIVE: continue
            if check and check.count(sel['color']):
                return False
            check.append(sel['color'])
        return True
