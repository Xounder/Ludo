import pygame

from util.input_management import InputManagement

import resource.settings as config

from util.painter import ClickRect, Painter

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

        self.painter = Painter()

    def init(self) -> None:
        """
        Inicializa as variáveis da tela de início, incluindo os seletores de cor e jogador
        """
        self.players = []
        self.active = True
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
        self.start_button = ClickRect(surf_size=(90, 60),
                                      rect_pos=(config.SCREEN_WIDTH/2 + 40, config.SCREEN_HEIGHT/2 - 15),
                                      d=3,
                                      topleft=True)
        # Color Selection Button
        self.color_selection = []
        # Player Selection Button
        self.player_selection = []
        pos = [40, 95]
        for i in range(4):
            # Color
            self.color_selection.append(ClickRect(surf_size=(20, 20), 
                                                  rect_pos=(self.pos[0] + pos[0], self.pos[1] + pos[1]),
                                                  r=10,
                                                  center=True))
            # Player
            self.player_selection.append(ClickRect(surf_size=(100, 30),
                                                   rect_pos=(self.pos[0] + pos[0] + 20, self.pos[1] + pos[1] - 15),
                                                   d=2,
                                                   topleft=True))
            pos[1] += 40

    def draw(self) -> None:
        """
        Desenha a tela de início, incluindo botões e seletores de cor e jogador
        """
        Painter.draw_rect(screen=self.screen, size=self.size, pos=self.pos, d=10)

        b_c = 'green' if self.is_start_game() else 'red'
        self.start_button.draw_animated_rect(self.screen, b_color=[b_c, 'gray'])
            
        for i in range(4):
            self.draw_selector(i)

        self.draw_texts()

    def draw_selector(self, id:int) -> None:
        """
        Desenha o seletor de cor e jogador para um índice específico

        Args:
            id (int): O índice do seletor a ser desenhado
        """
        atual_sel = self.selectors[id]
        c = (['gray', 'gray'] if atual_sel['player'] == config.INACTIVE 
                             else ['black', config.colors[atual_sel['color']]])

        self.color_selection[id].draw_animated_circle(screen=self.screen, colors=c)
        self.player_selection[id].draw_animated_rect(screen=self.screen, f_color='black')

    def draw_texts(self) -> None:
        Painter.blit_text_shadow(screen=self.screen,
                                 text='L U D O', 
                                 color='red', 
                                 pos=(config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2 - 85), 
                                 back_color='black', 
                                 center=True)

        Painter.blit_text_shadow(screen=self.screen,
                                 text='PLAY', 
                                 color='black', 
                                 pos=self.start_button.get_rect(center=True), 
                                 back_color='white', 
                                 center=True)
        
        for i, sel in enumerate(self.selectors):
            Painter.blit_text_shadow(screen=self.screen,
                                     text=config.player_status[sel['player']], 
                                     color=config.colors[sel['color']], 
                                     pos=self.player_selection[i].get_rect(center=True), 
                                     back_color='black', 
                                     center=True,
                                     font_size=26)
            
            pos = self.player_selection[i].get_rect(midright=True)
            Painter.blit_text_shadow(screen=self.screen,
                                     text=f'P{i+1}', 
                                     color=config.colors[sel['color']], 
                                     pos=(pos[0] + 10, pos[1]), 
                                     back_color='black', 
                                     center=True,
                                     font_size=24)

    def update(self) -> None:
        """
        Atualiza a tela de início, verificando a interação do usuário com os botões e seletores
        """
        if InputManagement.mouse_is_pressed():
            if self.start_button.is_rect_collide_point(InputManagement.cursor):
                self.active = not self.is_start_game()
            else:
                for i, b_color in enumerate(self.color_selection):
                    if self.selectors[i]['player'] == config.INACTIVE: continue
                    if b_color.is_rect_collide_point(InputManagement.cursor):
                        self.selectors[i]['color'] = (self.selectors[i]['color'] + 1) % len(config.colors)
                        return

                for i, ply_sel in enumerate(self.player_selection):
                    if ply_sel.is_rect_collide_point(InputManagement.cursor):
                        self.selectors[i]['player'] = (self.selectors[i]['player'] + 1) % 3
                        break
            
    def is_start_game(self) -> bool:
        """
        Verifica se o jogo pode começar, ou seja, se todos os jogadores selecionados têm cores únicas

        Returns:
            bool: Retorna True se o jogo pode começar, caso contrário, False
        """
        check_color = []
        check_player = []
        for sel in self.selectors:
            if sel['player'] == config.INACTIVE: continue
            if check_color and check_color.count(sel['color']): return False
            check_color.append(sel['color'])
            check_player.append(sel['player'])
        if len(check_color) >= 2 and check_player.count(config.PLAYER) >= 1: return True
        return False
