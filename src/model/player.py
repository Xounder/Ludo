import pygame

from model.piece import Piece
import resource.settings as config
from util.input_management import InputManagement
from model.dice import Dice

class Player:
    def __init__(self, color:str) -> None:
        """
        Inicializa um jogador com a cor especificada e cria quatro peças para o jogador 
        Define a peça atual e o estado do jogo

        Args:
            color (str): Cor do jogador
        """
        self.color = color
        self.pieces = [Piece(id=i, 
                             color=self.color, 
                             lobby_pos=config.lobby_pos[self.color][i]) 
                             for i in range(4)] 
        self.atual_piece = self.pieces[0]
        self.played = False
        self.check_auto = True

    def move_to_lobby(self, piece:int) -> None:
        """
        Move a peça especificada de volta para o lobby

        Args:
            piece (int): Índice da peça a ser movida para o lobby
        """
        self.pieces[piece].move_to_lobby()

    def play_again(self) -> None:
        """
        Reinicia o estado do jogador para o próximo turno, permitindo nova jogada e ativando a verificação automática
        """
        self.played = False
        self.check_auto = True

    def is_one_out(self) -> bool:
        """
        Verifica se pelo menos uma peça do jogador está fora do lobby

        Returns:
            bool: Retorna True se pelo menos uma peça estiver fora do lobby, caso contrário, False
        """
        for p in self.pieces:
            if not p.is_lobby: return True
        return False
    
    def is_only1_out(self) -> bool:
        """
        Verifica se somente uma peça do jogador está fora do lobby

        Returns:
            bool: Retorna True se apenas uma peça estiver fora do lobby, caso contrário, False
        """
        return True if len([1 for p in self.pieces if not p.is_lobby]) == 1 else False

    def is_only1_piece_to_move(self, value:Dice) -> bool:
        """
        Verifica se somente uma peça do jogador pode ser movida com o valor atual do dado

        Args:
            value (Dice): Valor do dado rolado

        Returns:
            bool: Retorna True se somente uma peça pode ser movida, caso contrário, False
        """ 
        p = [p.id for p in self.pieces 
                if not p.is_lobby and p.steps + value <= config.MAX_PIECE_STEPS or p.is_lobby and value == 6]
        if len(p) == 1:
            self.atual_piece = self.pieces[p[0]]
            return True
        return False
    
    def is_win(self) -> bool:
        """
        Verifica se o jogador ganhou o jogo, ou seja, se todas as peças do jogador atingiram o objetivo

        Returns:
            bool: Retorna True se todas as peças atingiram o objetivo, caso contrário, False
        """
        return True if len([1 for p in self.pieces if p.goal_achieved]) == 4 else False
    
    def move_piece(self, moves:int) -> None:
        """
        Move a peça atual do jogador pelo número de casas especificado

        Args:
            moves (int): Número de casas a serem movidas
        """
        self.atual_piece.move(moves)
    
    def get_pieces_pos(self) -> list:
        """
        Obtém as posições atuais de todas as peças do jogador

        Returns:
            list: Lista contendo as posições atuais de todas as peças do jogador
        """
        return [self.pieces[i].get_atual_pos() for i in range(4)]
    
    def get_atual_piece_pos(self) -> list:
        """
        Obtém a posição atual da peça que está sendo controlada pelo jogador

        Returns:
            list: Posição atual da peça controlada pelo jogador
        """
        return self.atual_piece.get_atual_pos()
    
    def get_piece_pos(self, piece:int) -> list:
        """
        Obtém a posição atual de uma peça específica do jogador

        Args:
            piece (int): Índice da peça

        Returns:
            list: Posição atual da peça especificada
        """
        return self.pieces[piece].get_atual_pos()

    def draw(self) -> None:
        """
        Desenha todas as peças do jogador na tela
        """
        for p in self.pieces: p.draw()

    def update(self, dice:Dice) -> None:
        """
        Atualiza o estado do jogador com base no valor do dado e na entrada do jogador

        Args:
            dice (Dice): Objeto do dado com o valor rolado
        """
        if dice.rolled and self.check_auto:
            self.check_auto = False
            self.played = self.is_auto_play(dice)
        self.input(dice)

    def input(self, dice:Dice) -> None:
        """
        Processa a entrada do jogador com base no estado do dado e na posição do cursor

        Args:
            dice (Dice): Objeto do dado com o valor rolado
        """
        if InputManagement.mouse_is_pressed():
            if dice.to_roll:
                dice.is_collide(InputManagement.cursor)
            else:
                if not dice.rolled: return

                if not self.played:
                    for p in self.pieces:
                        if p.is_collide(InputManagement.cursor, dice.value):
                            self.atual_piece = p
                            self.played = True
                            break
                
    def is_auto_play(self, dice:Dice) -> bool:
        """
        Determina se o jogador deve realizar a jogada automaticamente com base no valor do dado e no estado das peças

        Args:
            dice (Dice): Objeto do dado com o valor rolado

        Returns:
            bool: Retorna True se o jogador deve realizar a jogada automaticamente, caso contrário, False
        """
        if not self.is_one_out(): # nenhuma peça fora do lobby
            if dice.is_max_value(): return False
            return True
        else:
            if self.is_only1_out(): # somente uma peça fora do lobby
                if dice.is_max_value(): return False
                self.atual_piece.move(dice.value)                
                return True
            else: 
                if self.is_only1_piece_to_move(dice.value): # somente uma peça é possivel de mover
                    self.move_piece(dice.value)
                    return True
                return False
    