import pygame
import os

class SoundManager:
    
    atual_sound = None
    all_sounds = {}

    @staticmethod
    def initialize():
        SoundManager.load_sounds()

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
                SoundManager.all_sounds[sound_name] = s

    @staticmethod
    def play_sound(sound_name):
        if SoundManager.atual_sound: 
            SoundManager.all_sounds[SoundManager.atual_sound].stop()
        SoundManager.all_sounds[sound_name].play()
        SoundManager.atual_sound = sound_name
