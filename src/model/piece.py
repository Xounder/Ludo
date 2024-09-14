import pygame
import resource.settings as config

from model.map import Map
from model.dice import Dice

class Piece:
    def __init__(self, id:int, color:str, lobby_pos:list) -> None:
        """
        Inicializa a peça com um ID, cor e posição inicial no lobby
        Configura o estado da peça e carrega a imagem associada
        
        Args:
            id (int): Identificador único da peça
            color (str): Cor da peça
            lobby_pos (list): Posição da peça no lobby
        """
        self.screen = pygame.display.get_surface()
        self.id = id
        self.color = color
        self.lobby_pos = lobby_pos
        self.first_cell = config.map_fcell[self.color]
        self.atual_cell = self.first_cell
        self.goal_achieved = False
        self.is_lobby = True
        self.steps = 0
        self.eliminate = False
        self.PIECE_STEPS_GOAL = config.PIECE_STEPS_GOAL
        self.assets()
    
    def assets(self) -> None:
        """
        Carrega a imagem da peça e configura o retângulo de colisão com base na posição inicial no lobby
        """
        self.image = pygame.image.load(f'img/{self.color}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=self.to_tile(self.lobby_pos))

    def get_atual_pos(self, step=-1) -> list:
        """
        Retorna a posição atual da peça com base no número de passos dados
        Se `step` não for fornecido, usa o número de passos atual
        
        Args:
            step (int, opcional): Número de passos para calcular a posição. Se não fornecido, usa o número de passos atual

        Returns:
            list: Coordenadas da posição da peça.
        """
        step = step if step != -1 else self.steps
        if step <= config.PIECE_STEPS_GOAL:
            return config.map_steps[self.atual_cell] if not self.is_lobby else self.lobby_pos
        else:
            return config.map_goal_steps[self.color][self.atual_cell]
    
    def is_playable(self, dice:Dice) -> bool:
        """
        Determina se a peça pode ser movida com base no valor do dado e no número de passos dados
        
        Args:
            dice (Dice): Objeto do dado que contém o valor atual do dado

        Returns:
            bool: Retorna True se a peça pode ser movida, caso contrário, False
        """
        if self.steps + dice.value <= config.MAX_PIECE_STEPS:
            if self.is_lobby:
                return dice.is_max_value()
            return True
        return False

    def update_rect(self):
        """
        Atualiza a posição do retângulo da peça com base na sua posição atual no tabuleiro
        """
        l = (config.map_steps[self.atual_cell] if self.steps < 
                     self.PIECE_STEPS_GOAL else config.map_goal_steps[self.color][self.atual_cell])
        self.rect.topleft = self.to_tile(l)
        
    def to_tile(self, l:list):
        """
        Converte as coordenadas de uma célula em pixels, ajustando para o tamanho do tile e uma margem.
        
        Args:
            l (list): Coordenadas da célula no tabuleiro.

        Returns:
            list: Coordenadas da célula em pixels.
        """
        return list(map(lambda x: x * config.TILE_SIZE + 8, l))

    def move_to_lobby(self) -> None:
        """
        Move a peça de volta para o lobby e redefine seu estado para a posição inicial e o número de passos como 0
        """
        Map.add_redraw_map(self.get_atual_pos())
        self.rect.topleft = self.to_tile(self.lobby_pos)
        self.atual_cell = self.first_cell
        self.steps = 0
        self.is_lobby = True

    def leave_lobby(self) -> None:
        """
        Move a peça para fora do lobby e posiciona-a no início do caminho do tabuleiro
        Define o número de passos como 1 e atualiza seu estado
        """
        Map.add_redraw_map(self.lobby_pos)
        self.rect.topleft = self.to_tile(config.map_steps[self.first_cell])
        self.steps = 1
        self.is_lobby = False

    def draw(self) -> None:
        """
        Desenha a peça na tela na posição atual usando a imagem carregada
        """
        self.screen.blit(self.image, self.rect)

    def move(self, moves:int) -> bool:
        """
        Move a peça um número específico de passos
        Atualiza o estado da peça e a posição no tabuleiro
        
        Args:
            moves (int): Número de passos a serem movidos pela peça

        Returns:
            bool: Retorna True se a peça foi movida, caso contrário, False
        """
        moved = False
        if self.steps >= self.PIECE_STEPS_GOAL:
            if self.steps + moves <= config.MAX_PIECE_STEPS:
                self.steps += moves        
                moved = True
        else:
            self.steps += moves
            moved = True

        if moved:
            Map.add_redraw_map(self.get_atual_pos(self.steps - moves))
            self.change_atual_cell(moves)
            self.update_rect()
            self.check_goal()
        return moved
                    
    def change_atual_cell(self, moves:int) -> None:
        """
        Atualiza a célula atual da peça com base no número de passos dados
        Ajusta a célula se a peça alcançar ou exceder o número máximo de passos
        
        Args:
            moves (int): Número de passos a serem dados
        """
        self.atual_cell += moves
        if self.steps >= self.PIECE_STEPS_GOAL:
            self.atual_cell = self.steps - self.PIECE_STEPS_GOAL
        else:
            if self.atual_cell >= self.PIECE_STEPS_GOAL:
                self.atual_cell = self.atual_cell - self.PIECE_STEPS_GOAL
    
    def check_goal(self) -> None:
        """
        Verifica se a peça alcançou o objetivo final e marca a meta como alcançada se for o caso
        """
        if self.steps == config.MAX_PIECE_STEPS:
            self.goal_achieved = True      

    def is_collide(self, mouse_pos:list, dice_value:int) -> bool:
        """
        Verifica se a peça foi clicada na tela e, se não estiver no lobby, move a peça de acordo com o valor do dado
        Se estiver no lobby, a peça sai do lobby
        
        Args:
            mouse_pos (list): Coordenadas do clique do mouse
            dice_value (int): Valor do dado que será usado para mover a peça

        Returns:
            bool: Retorna True se a peça foi clicada e movida, caso contrário, False
        """
        if self.rect.collidepoint(mouse_pos):
            if not self.is_lobby:
                return self.move(dice_value)
            else:
                self.leave_lobby()
                return True
        return False
    