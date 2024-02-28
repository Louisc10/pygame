import pygame

class SoundManager():
    def __init__(self):
        pygame.mixer.init()
        self.musics = {
            'start' : pygame.mixer.Sound('./tutorial/assets/sounds/title.wav'),
            'level1' : pygame.mixer.Sound('./tutorial/assets/sounds/level1.wav'),
            'level2' : pygame.mixer.Sound('./tutorial/assets/sounds/level2.wav'),
            'level3' : pygame.mixer.Sound('./tutorial/assets/sounds/level3.wav'),
            'ending' : pygame.mixer.Sound('./tutorial/assets/sounds/ending.wav'),
        }
        
    def play_music(self, music_name):
        self.musics[music_name].set_volume(0.2)
        self.musics[music_name].play(loops=-1)
        
    def stop_all_music(self):
        for music in self.musics:
            self.musics[music].stop()