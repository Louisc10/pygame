import pygame
from constant import SKY_WIDTH, SKY_HEIGHT

class Sky (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sky1_surface = pygame.image.load('./tutorial/assets/images/sky_1.png').convert()
        sky2_surface = pygame.image.load('./tutorial/assets/images/sky_2.png').convert()
        sky3_surface = pygame.image.load('./tutorial/assets/images/sky_3.png').convert()
        self.frame = [sky1_surface, sky2_surface, sky3_surface]
        self.index = 0
        self.image = self.frame[self.index]
        self.image = pygame.transform.scale(self.image, (SKY_WIDTH,SKY_HEIGHT))
        self.rect = self.image.get_rect(topleft = (0,0))
    
    def change_bg(self, state):
        self.index = state
        self.image = self.frame[self.index]
        self.image = pygame.transform.scale(self.image, (SKY_WIDTH,SKY_HEIGHT))