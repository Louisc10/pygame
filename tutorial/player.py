import pygame
from constant import PLAYER_POS_X, GROUND_POS_Y, GRAVITY, JUMP_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1_surface = pygame.image.load('./tutorial/assets/images/player/player_walk_1.png').convert_alpha()
        player_walk_2_surface = pygame.image.load('./tutorial/assets/images/player/player_walk_2.png').convert_alpha()
        self.walk = [player_walk_1_surface, player_walk_2_surface]
        self.jump = pygame.image.load('./tutorial/assets/images/player/jump.png').convert_alpha()
        self.index = 0
        
        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(bottomleft = (PLAYER_POS_X, GROUND_POS_Y))
        self.gravity = 0
        
        self.jump_sound = pygame.mixer.Sound('./tutorial/assets/sounds/jump.mp3')
        self.jump_sound.set_volume(0.2)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == GROUND_POS_Y:
            print('jump')
            self.gravity -= GRAVITY * JUMP_HEIGHT
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity += GRAVITY
        self.rect.y += self.gravity
        if(self.rect.bottom >= GROUND_POS_Y): 
            self.rect.bottom = GROUND_POS_Y
            self.gravity = 0
            
    def animation_state(self):
        if self.rect.bottom == GROUND_POS_Y:
            self.image = self.walk[int(self.index)]
            self.index += 0.1
            if self.index >= len(self.walk): self.index = 0
        else:
            self.image = self.jump
            
    def reset(self):
        self.rect.bottom = GROUND_POS_Y
        self.gravity = 0
        self.index = 0
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        return super().update()
