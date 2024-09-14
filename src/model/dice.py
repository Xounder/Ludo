import pygame
from random import randint

import resource.settings as config
from util.timer_management import TimerManagement

class Dice:
    def __init__(self) -> None:
        """
        Inicializa o dado com o valor máximo e configura o estado inicial 
        Carrega as imagens do dado e define o retângulo de exibição
        """
        self.screen = pygame.display.get_surface()
        self.MAX_VALUE = 6
        self.value = self.MAX_VALUE
        self.to_roll = True
        self.rolled = False
        self.timer_activated = False
        self.atual_frame = 0
        self.assets()

    def assets(self) -> None:
        """
        Carrega as imagens dos dados e define o retângulo de exibição 
        Adiciona um temporizador para animação
        """
        self.dices_surf = [pygame.image.load(f'img/dice/dice{i+1}.png').convert_alpha() for i in range(6)]
        self.image = self.dices_surf[self.value-1]
        self.rect = self.image.get_rect(center=(config.SCREEN_WIDTH/2 + 1, config.SCREEN_HEIGHT/2 + 1))
        TimerManagement.add_timer('animation_timer', 0.4)

    def is_max_value(self) -> bool:
        """
        Verifica se o valor do dado é o máximo (6).

        Returns:
            bool: Retorna True se o valor do dado for 6, caso contrário, False.
        """
        return True if self.value == self.MAX_VALUE else False

    def roll(self) -> None:
        """
        Rola o dado, atribuindo um novo valor aleatório e atualizando a imagem exibida
        """
        self.value = randint(1, self.MAX_VALUE)
        self.image = self.dices_surf[self.value-1]

    def reset(self) -> None:
        """
        Reinicia o estado do dado, definindo-o para ser lançado novamente
        """
        self.to_roll = True
        self.rolled = False
        self.timer_activated = False

    def draw(self) -> None:
        """
        Desenha a imagem atual do dado na tela na posição definida
        """
        self.screen.blit(self.image, self.rect)

    def update(self) -> None:
        """
        Atualiza o estado do dado com base no temporizador
        Se o temporizador está ativo, executa a animação
        Caso contrário, se o temporizador foi ativado, rola o dado
        """
        if TimerManagement.is_run('animation_timer'):
            self.animate()
        else:
            if self.timer_activated:
                self.rolled = True
                self.timer_activated = False
                self.roll()

    def animate(self) -> None:
        """
        Atualiza a imagem do dado para criar uma animação visual de rotação
        """
        self.atual_frame += 0.15
        if self.atual_frame > len(self.dices_surf)-1:
            self.atual_frame = 0
        self.image = self.dices_surf[int(self.atual_frame)]
        
    def is_collide(self, mouse_pos:list) -> bool:
        """
        Verifica se a posição do mouse colide com o retângulo do dado. Se houver colisão, ativa o temporizador de animação e define o estado do dado para ser rolado.
        
        Args:
            mouse_pos (list): Coordenadas do clique do mouse.

        Returns:
            bool: Retorna True se houve colisão, caso contrário, False.
        """
        if self.rect.collidepoint(mouse_pos):
            TimerManagement.active_timer('animation_timer')
            self.timer_activated = True
            self.to_roll = False    
            return True
        return False