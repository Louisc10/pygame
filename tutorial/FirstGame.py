import pygame
from sys import exit
from random import randint, choice

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_POS_Y = 300
FLY_POS_Y = 200
PLAYER_POS_X = 100
GAME_NAME = "Jumper Game"
OBSTACLE_SPEED = 5
GRAVITY = 0.3
JUMP_HEIGHT = 30
PRIMARY_COLOR = '#8bcfba'

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
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == GROUND_POS_Y:
            print('jump')
            self.gravity -= GRAVITY * JUMP_HEIGHT
            
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
        self.rect = self.image.get_rect(bottomleft = (randint(SCREEN_WIDTH, SCREEN_WIDTH+200), pos_y))
    
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
        

def init():
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,GROUND_POS_Y))
    pygame.draw.rect(screen, '#8bcfba', title_background_rect)
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)

def display_score():
    global screen, start_time
    current_time = (int)((pygame.time.get_ticks()- start_time)/1000)
    score_text = font.render(f'Score: { current_time }', True, PRIMARY_COLOR)
    score_rect = score_text.get_rect(center = (SCREEN_WIDTH/2, 60))
    screen.blit(score_text, score_rect)
    return current_time

def sprite_collision():
    game_active = True
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        print("You Lose!")
        game_active = False
        screen.blit(lose_text, lose_rect)
        screen.blit(start_text, start_rect)
    return game_active

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)
game_active = False

clock = pygame.time.Clock()
font = pygame.font.Font('./tutorial/assets/fonts/Pixeltype.ttf', 30)
start_time = 0

title_text = font.render(GAME_NAME, True, 'White')
title_rect = title_text.get_rect(center = (SCREEN_WIDTH/2, 30))
title_background_rect = title_rect.scale_by(1.2, 1.5)

start_text = font.render('Press SPACE to play', True, PRIMARY_COLOR)
start_rect = start_text.get_rect(center = (SCREEN_WIDTH/2, 250))

lose_text = font.render('YOU LOSE', True, 'RED')
lose_rect = lose_text.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

sky_surface = pygame.image.load('./tutorial/assets/images/sky.png').convert()
ground_surface = pygame.image.load('./tutorial/assets/images/ground.png').convert()

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if  game_active:                    
            if event.type == obstacle_timer:
                print("Create Obstacle!")
                obstacles.add(Obstacle(choice(['snail', 'fly', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
                obstacles.empty()
                player.sprite.reset()
                init()
            
    if game_active == True:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,GROUND_POS_Y))
        
        pygame.draw.rect(screen, PRIMARY_COLOR, title_background_rect)
        screen.blit(title_text, title_rect)
        display_score()
        
        player.draw(screen)
        player.update()
        
        obstacles.draw(screen)
        obstacles.update()
        
        game_active = sprite_collision()
        
    pygame.display.update()
    clock.tick(60)