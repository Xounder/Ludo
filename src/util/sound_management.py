import pygame
import os

from enum import Enum

class SoundManagement:
    
    atual_sound = None

    @staticmethod
    def initialize():
        SoundManagement.load_sounds()

    @staticmethod
    def load_sounds():
        sounds_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../sounds'))
        for root, __, files in os.walk(sounds_dir):
            for sound in files:
                sound_path = os.path.join(root, sound)
                sound_name = sound.split('.')[0]
                # Define o som como um atributo da classe
                s = pygame.mixer.Sound(sound_path)
                s.set_volume(0.2)
                setattr(SoundManagement, sound_name, s)

    @staticmethod
    def play_sound(sound):
        if SoundManagement.atual_sound: SoundManagement.atual_sound.stop()
        
        sound.play()
        SoundManagement.atual_sound = sound
