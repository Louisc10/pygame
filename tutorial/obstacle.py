import pygame
from random import randint
from constant import GROUND_POS_Y, FLY_POS_Y, OBSTACLE_SPEED, SCREEN_WIDTH

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "snail":
            snail_1_surface = pygame.image.load('./tutorial/assets/images/snail/snail1.png').convert_alpha()
            snail_2_surface = pygame.image.load('./tutorial/assets/images/snail/snail2.png').convert_alpha()
            self.frame = [snail_1_surface, snail_2_surface]
            pos_y = GROUND_POS_Y
        elif type == "fly":
            fly_1_surface = pygame.image.load('./tutorial/assets/images/fly/fly1.png').convert_alpha()
            fly_2_surface = pygame.image.load('./tutorial/assets/images/fly/fly2.png').convert_alpha()
            self.frame = [fly_1_surface, fly_2_surface]
            pos_y = FLY_POS_Y
        self.index = 0
        self.type = type
        self.image = self.frame[self.index]
        self.rect = self.image.get_rect(bottomleft = (randint(SCREEN_WIDTH, SCREEN_WIDTH+150), pos_y))
    
    def movement(self):
        self.rect.x -= OBSTACLE_SPEED
            
    def animation_state(self):
        self.image = self.frame[int(self.index)]
        self.index += 0.1
        if self.index >= len(self.frame): self.index = 0
    
    def update(self):
        self.movement()
        self.animation_state()
        self.destroy()
        return super().update()
    
    def destroy(self):
        if(self.rect.right < 0): 
            self.kill()