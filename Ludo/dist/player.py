import pygame
from settings import *
from map import map
from timer import Timer

class Player:
    def __init__(self, id):
        self.display_surface = pygame.display.get_surface()
        self.player_id = id
        self.pieces = [0, 0, 0, 0]
        self.pieces_pos = []
        self.freedom = [False, False, False, False]        
        self.roll_again = False
        self.pieces_lobby_pos = players_lobby_pos[players_color[id]][:]
        self.choosed_piece = 0
        # pieces image
        piece_surf = pygame.image.load(f'img/{players_color[self.player_id]}.png').convert_alpha()
        self.piece_surf = [piece_surf for i in range(4)]        
        self.piece_rect = [self.piece_surf[i].get_rect(topleft= (0, 0)) for i in range(4)]
        self.piece_goto_lobby()
        # timer
        self.mouse_timer = Timer(0.7)

    def draw(self):
        for i in range(4):
            self.display_surface.blit(self.piece_surf[i], self.piece_rect[i])
            
    def piece_goto_lobby(self, all=True, choosed_piece=0):
        # coloca a(s) peça(s) no lobby 
        if all:
            self.pieces_pos = self.pieces_lobby_pos[:]
            self.pieces = [0, 0, 0, 0]
            for i in range (len(self.piece_rect)):
                self.change_rect_pos(self.pieces_lobby_pos, i)
        else:
            self.pieces_pos[choosed_piece] = self.pieces_lobby_pos[choosed_piece][:]
            self.pieces[choosed_piece] = 0
            self.change_rect_pos(self.pieces_lobby_pos, choosed_piece)

    def change_rect_pos(self, piece_pos, choosed_piece):
        self.piece_rect[choosed_piece].topleft = (8 + tile_size*piece_pos[choosed_piece][0],
                                                 8 + tile_size*piece_pos[choosed_piece][1])

    def piece_out_lobby(self):
        self.pieces[self.choosed_piece] = players_start[self.player_id]
        self.pieces_pos[self.choosed_piece] = players_start_pos[self.player_id][:]

    def move_piece(self, num_dice, all_players, atual_player):
        # movimenta a peça escolhida de acordo com o numero do DICE
        if self.pieces[self.choosed_piece] == 0:
            if num_dice == 6:
                self.piece_out_lobby()
        else:
            for i in range(num_dice):
                atual_piece = self.pieces[self.choosed_piece]
                if atual_piece == players_entry_heaven[self.player_id]:
                    self.pieces[self.choosed_piece] = players_start_heaven[self.player_id]
                    self.pieces_pos[self.choosed_piece] = players_start_heaven_pos[self.player_id][:]
                    self.change_rect_pos(self.pieces_pos, self.choosed_piece)
                if atual_piece < 52 or atual_piece > 100:
                    self.pieces[self.choosed_piece] += 1  
                    if atual_piece + 1 == players_end_heaven[self.player_id]:
                        self.freedom[self.choosed_piece] = True
                        self.roll_again = True
                        print('finish', self.roll_again, self.freedom, self.choosed_piece)
                else:
                    self.pieces[self.choosed_piece] = 1  
                    
                next_place = self.pieces[self.choosed_piece]
                x_piece = self.pieces_pos[self.choosed_piece][0]
                y_piece = self.pieces_pos[self.choosed_piece][1]
                y_change = 0
                x_change = 0
                
                if y_piece - 1 < 0: #limite em cima
                    if map[y_piece + 1][x_piece] == next_place: #baixo
                        y_change = 1
                    elif map[y_piece + 1][x_piece - 1] == next_place: # baixo-esquerda
                        y_change = 1
                        x_change = -1
                    elif map[y_piece + 1][x_piece + 1] == next_place: #baixo-direita
                        y_change = 1
                        x_change = 1
                    elif map[y_piece][x_piece + 1] == next_place: #direita
                        x_change = 1
                    elif map[y_piece][x_piece - 1] == next_place: #esquerda
                        x_change = -1
                        
                elif y_piece + 1 > len(map[0]) - 1: #limite em baixo
                    if map[y_piece - 1][x_piece] == next_place: #cima
                        y_change = -1
                    elif map[y_piece - 1][x_piece + 1] == next_place: #cima-direita
                        y_change = -1
                        x_change = 1
                    elif map[y_piece - 1][x_piece - 1] == next_place: #cima-esquerda
                        y_change = -1
                        x_change = -1
                    elif map[y_piece][x_piece + 1] == next_place: #direita
                        x_change = 1
                    elif map[y_piece][x_piece - 1] == next_place: #esquerda
                        x_change = -1
                
                elif x_piece - 1 < 0: # limite esquerda
                    if map[y_piece][x_piece + 1] == next_place: #direita
                        x_change = 1
                    elif map[y_piece - 1][x_piece + 1] == next_place: #cima-direita
                        y_change = -1
                        x_change = 1
                    elif map[y_piece + 1][x_piece + 1] == next_place: #baixo-direita
                        y_change = 1
                        x_change = 1
                    elif map[y_piece + 1][x_piece] == next_place: #baixo
                        y_change = 1
                    elif map[y_piece - 1][x_piece] == next_place: #cima
                        y_change = -1

                elif x_piece + 1 > len(map) - 1:
                    if map[y_piece][x_piece - 1] == next_place: #esquerda
                        x_change = -1
                    elif map[y_piece + 1][x_piece - 1] == next_place: # baixo-esquerda
                        y_change = 1
                        x_change = -1
                    elif map[y_piece - 1][x_piece - 1] == next_place: #cima-esquerda
                        y_change = -1
                        x_change = -1
                    elif map[y_piece + 1][x_piece] == next_place: #baixo
                        y_change = 1
                    elif map[y_piece - 1][x_piece] == next_place: #cima
                        y_change = -1

                else:
                    if map[y_piece + 1][x_piece] == next_place: #baixo
                        y_change = 1
                    elif map[y_piece][x_piece + 1] == next_place: #direita
                        x_change = 1
                    elif map[y_piece - 1][x_piece] == next_place: #cima
                        y_change = -1
                    elif map[y_piece][x_piece - 1] == next_place: #esquerda
                        x_change = -1
                    elif map[y_piece + 1][x_piece - 1] == next_place: # baixo-esquerda
                        y_change = 1
                        x_change = -1
                    elif map[y_piece - 1][x_piece + 1] == next_place: #cima-direita
                        y_change = -1
                        x_change = 1
                    elif map[y_piece - 1][x_piece - 1] == next_place: #cima-esquerda
                        y_change = -1
                        x_change = -1
                    elif map[y_piece + 1][x_piece + 1] == next_place: #baixo-direita
                        y_change = 1
                        x_change = 1
                self.pieces_pos[self.choosed_piece][0] += x_change
                self.pieces_pos[self.choosed_piece][1] += y_change
                
        self.change_rect_pos(self.pieces_pos, self.choosed_piece)
        self.collide_enemy_piece(all_players, atual_player)

    def input(self, num_dice):
        # escolher a peça
        if not self.mouse_timer.run:
            if pygame.mouse.get_pressed()[0]:
                mouse_surf = pygame.Surface((5, 5))
                mouse_rect = mouse_surf.get_rect(center= (pygame.mouse.get_pos()))
                for i, piece_rect in enumerate(self.piece_rect):
                    if piece_rect.colliderect(mouse_rect):
                        if self.pieces[i] == 0 and not num_dice == 6:
                            return False
                        if self.freedom[i]:
                            return False
                        if self.pieces[i] > 100 and self.pieces[i] + num_dice > players_end_heaven[self.player_id]:
                            return False
                        self.choosed_piece = i
                        self.mouse_timer.active()
                        return True
        
    def collide_enemy_piece(self, all_players, atual_player):
        for ply_id, player in enumerate(all_players):
            if ply_id == atual_player:
                continue
            for index, piece_place in enumerate(player.pieces):
                if piece_place == self.pieces[self.choosed_piece]:
                    if not self.cant_collide_enemy_piece(piece_place):
                        player.piece_goto_lobby(all=False, choosed_piece=index)
                        self.roll_again = True

    def cant_collide_enemy_piece(self, piece_place):
        for cell in star_cells:
            if cell == piece_place:
                return True
        for start_cell in players_start:
            if start_cell == piece_place:
                return True

    def is_move_pieces_heaven(self, num_dice):
        pieces_heaven = 0
        can_play = False
        for piece in self.pieces:
            if piece > 100:
                pieces_heaven += 1
                if piece + num_dice <= players_end_heaven[self.player_id]:
                    can_play = True                
        return can_play, pieces_heaven
        
    def find_piece_out(self):
        piece_out = -1
        piece_out_heaven = -1
        for i, piece in enumerate(self.pieces):
            if piece > 0:
                if piece < 100: 
                    piece_out = i
                else:
                    piece_out_heaven = i
        return piece_out if piece_out != -1 else piece_out_heaven
    
    def choose_piece(self, num_dice):
        pieces_in_lobby = self.pieces.count(0)
        pieces_out_lobby = len(self.pieces) - pieces_in_lobby
        can_move_heaven, pieces_heaven = self.is_move_pieces_heaven(num_dice)

        if num_dice == 6:
            if pieces_out_lobby - pieces_heaven == 1 and not can_move_heaven and pieces_in_lobby == 0:
                self.choosed_piece = self.find_piece_out()
                return 0
            else:
                return 1       
        else:
            if ((pieces_out_lobby == 1 and (pieces_out_lobby - pieces_heaven != 0 or can_move_heaven)) or 
                                                (pieces_out_lobby - pieces_heaven == 1 and not can_move_heaven)):
                self.choosed_piece = self.find_piece_out()
                return 0
            elif pieces_out_lobby == 0 or (not can_move_heaven and pieces_out_lobby - pieces_heaven == 0):
                return -1
            else:
                return 1
        
    def update(self, num_dice, all_players, atual_player):
        if self.mouse_timer.run:
            self.mouse_timer.update()

        if self.choose_piece(num_dice) == 0:
            self.move_piece(num_dice, all_players, atual_player)
            return True
        elif self.choose_piece(num_dice) == 1:
            if self.input(num_dice):
                self.move_piece(num_dice, all_players, atual_player)
                return True
        else:
            return True
