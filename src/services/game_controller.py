import pygame
from model.map import Map
from model.player import Player
from model.dice import Dice

import resource.settings as config

from util.painter import Painter
from services.updater import Updater
from util.sound_management import SoundManagement

import random
import time

class GameController:
    def __init__(self) -> None:
        """
        Inicializa o controlador do jogo, configurando a tela, o mapa, o dado e o estado do jogo

        Attributes:
            screen (pygame.Surface): Superfície de exibição do jogo
            map (Map): Instância da classe Map para gerenciar o mapa do jogo
            dice (Dice): Instância da classe Dice para gerenciar o dado
            active (bool): Flag que indica se o jogo está em execução
        """
        self.screen = pygame.display.get_surface()
        self.map = Map()
        self.dice = Dice()
        self.active = False   
        self.active_end_game_music = True
        self.timer_name = 'end-game_timer'
        Updater.add_to_animate(self.timer_name, 2.5)     

    def draw_map(self) -> None:
        """
        Desenha o mapa do jogo na tela
        """
        self.map.draw_map()

    def start_game(self, players:dict) -> None:
        """
        Inicia o jogo configurando os jogadores e o estado inicial

        Args:
            players (dict): Dicionário contendo informações sobre os jogadores, incluindo cor e status
        """
        self.players = []
        for ply in players:
            if ply['player'] == config.INACTIVE: continue
            if ply['player'] == config.PLAYER:
                p = Player(config.colors[ply['color']]) 
            else:
                pass
            self.players.append(p)

        self.ply_id = 0
        self.atual_ply = self.players[self.ply_id]
        self.draw_map()
        self.active = True

    def next_ply(self) -> None:
        """
        Avança para o próximo jogador e reinicia o estado do jogador atual
        """
        self.ply_id = (self.ply_id + 1) % len(self.players)
        self.atual_ply = self.players[self.ply_id]
        self.play_again()

    # DRAW
    def draw_ply_indicator(self) -> None:
        """
        Desenha o indicador do jogador atual na tela, com base no estado do dado (se lançado ou não)
        """
        if not self.dice.rolled:
            self.draw_dice_to_roll()
        else:
            self.draw_atual_ply_color()

    def draw_dice_to_roll(self) -> None:
        """
        Desenha a indicação para rolar o dado, mostrando a cor do jogador atual e uma borda ao redor do dado
        """
        rect_tl = self.dice.rect.topleft
        pygame.draw.rect(self.screen, self.atual_ply.color, (rect_tl[0], rect_tl[1], config.TILE_SIZE, config.TILE_SIZE), 4)
        pygame.draw.rect(self.screen, 'black', (rect_tl[0], rect_tl[1], config.TILE_SIZE, config.TILE_SIZE), 1)

    def draw_atual_ply_color(self) -> None:
        """
        Desenha a cor do jogador atual no centro do dado após ele ser rolado
        """
        rect_c = self.dice.rect.center
        pygame.draw.rect(self.screen, self.atual_ply.color, (rect_c[0] + 8, rect_c[1] + 8, 8, 8), 0)
        pygame.draw.rect(self.screen, 'black', (rect_c[0] + 8, rect_c[1] + 8, 8, 8), 1)

    def draw_ply_piece(self) -> None:
        """
        Desenha as peças do jogador atual que podem ser movidas, se o dado já foi rolado
        """
        if not self.dice.rolled: return
        if self.atual_ply.atual_piece.moved: return
        for p in self.atual_ply.pieces:
            if not p.is_playable(self.dice): continue  
            pos = p.rect.center
            pygame.draw.circle(self.screen, 'black', (pos[0] + 1, pos[1] + 1), 5, 0)

    def draw_end_game(self, color:str) -> None:
        size = (300, 150)
        pos = (config.SCREEN_WIDTH/2 - size[0]/2, config.SCREEN_HEIGHT/2 - size[1]/2)
        Painter.draw_rect(screen=self.screen, 
                          size=size, 
                          pos=pos,
                          d=5,
                          f_color=color,
                          b_color='gray')
        
        pos = (config.SCREEN_WIDTH/2, config.SCREEN_HEIGHT/2)
        Painter.blit_text_shadow(screen=self.screen,
                                 text=f'PLAYER{self.ply_id+1}', 
                                 color=self.atual_ply.color, 
                                 pos=(pos[0], pos[1]-20), 
                                 back_color='black', 
                                 center=True,
                                 font_size=42)
        
        Painter.blit_text_shadow(screen=self.screen,
                                 text=f'WIN!', 
                                 color='red', 
                                 pos=(pos[0], pos[1] + 20), 
                                 back_color='black', 
                                 center=True,
                                 font_size=42)
        
    def draw(self) -> None:
        """
        Desenha todos os elementos do jogo na tela
        """
        self.map.draw()
        self.dice.draw()
        self.draw_ply_indicator()
        for i in range(len(self.players)):
            if self.ply_id == i: continue
            self.players[i].draw()
        self.atual_ply.draw()
        self.draw_ply_piece()

    # UPDATE
    def update(self) -> None:
        """
        Atualiza o estado do jogo
        """
        if not self.atual_ply.played:
            self.atual_ply.update(self.dice)
        else:
            if not self.is_end_game():
                if self.is_end_turn():
                    self.next_ply()

    def play_again(self) -> None:
        """
        Reinicia o estado do jogador atual e o dado para permitir uma nova jogada
        """
        self.atual_ply.play_again()
        self.dice.reset()

    def animate(self) -> None:
        if self.active_end_game_music:
            self.active_end_game_music = False
            SoundManagement.play_sound(SoundManagement.won)
        self.draw_end_game(random.choice(config.colors))
        time.sleep(0.3)

    def callback(self) -> None:
        self.draw_map()
        self.active = False
        self.active_end_game_music = True

    def is_end_game(self) -> bool:
        """
        Verifica se o jogo terminou, ou seja, se o jogador atual ganhou

        Returns:
            bool: Retorna True se o jogador atual ganhou o jogo, caso contrário, False
        """
        if self.atual_ply.is_win():
            Updater.call_to_animate(self.timer_name, self.animate, self.callback)
            return True
        return False
    
    def is_end_turn(self) -> bool:
        """
        Verifica se o turno do jogador atual terminou 
        Se o dado mostrou o valor máximo ou uma peça foi eliminada, o turno termina

        Returns:
            bool: Retorna True se o turno deve terminar, caso contrário, False
        """
        if self.dice.is_max_value():
            self.is_eliminate_piece()
            self.play_again()
            return False
        elif self.atual_ply.atual_piece.goal_achieved:
            self.play_again()
            return False
        else:
            if self.is_eliminate_piece():
                self.play_again()
                return False
            return True
        
    def is_eliminate_piece(self) -> bool:
        """
        Verifica se uma peça do jogador atual deve ser eliminada e movida de volta para o lobby

        Returns:
            bool: Retorna True se alguma peça foi eliminada, caso contrário, False
        """
        # célula neutra
        if config.star_cells.count(self.atual_ply.get_atual_piece_pos()): return False
        if config.map_fcell_colors.count(self.atual_ply.get_atual_piece_pos()): return False

        again = False
        for i, ply in enumerate(self.players):
            if self.ply_id == i: continue
            for p in ply.pieces:
                if p.get_atual_pos() == self.atual_ply.get_atual_piece_pos():
                    p.move_to_lobby()
                    again = True
                    SoundManagement.play_sound(SoundManagement.eliminate)
        return again
