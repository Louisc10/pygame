#CREDITS:
#SPRITE: https://opengameart.org/content/platformer-art-pixel-edition
#MUSIC: https://opengameart.org/content/5-chiptunes-action

import pygame
from sys import exit
from random import randint, choice
from constant import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_POS_Y, LEVEL_CHANGE, PRIMARY_COLOR, GAME_NAME
from player import Player
from obstacle import Obstacle
from sky import Sky
from soundmanager import SoundManager

def init():
    sky.draw(screen)
    screen.blit(ground_surface, (0,GROUND_POS_Y))
    pygame.draw.rect(screen, '#8bcfba', title_background_rect)
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)
    sound_manager.stop_all_music()
    sound_manager.play_music('start')

def display_score():
    global screen, start_time
    current_time = (int)((pygame.time.get_ticks()- start_time)/1000)
    score_text = font.render(f'Score: { current_time }', True, PRIMARY_COLOR)
    score_rect = score_text.get_rect(center = (SCREEN_WIDTH/2, 60))
    screen.blit(score_text, score_rect)
    return current_time

def change_bg():
    global current_time, prev_time
    if prev_time != current_time:
        print(current_time, prev_time)
        if current_time % LEVEL_CHANGE == 0:
            state = int((current_time/LEVEL_CHANGE) % len(sky.sprite.frame))
            print(f"change background { state }")
            sky.sprite.change_bg(state)
            prev_time = current_time
            sound_manager.stop_all_music()
            
            track = ''
            match state:
                case 0:
                    track = 'level1'
                case 1:
                    track = 'level2'
                case 2:
                    track = 'level3'
            sound_manager.play_music(track)
    

def sprite_collision():
    game_active = True
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        print("You Lose!")
        game_active = False
        screen.blit(lose_text, lose_rect)
        screen.blit(start_text, start_rect)
        
        sound_manager.stop_all_music()
        sound_manager.play_music('ending')
    return game_active


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)
game_active = False
prev_time = current_time = 0
sound_manager = SoundManager()

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

ground_surface = pygame.image.load('./tutorial/assets/images/ground.png').convert()

player = pygame.sprite.GroupSingle()
player.add(Player())

sky = pygame.sprite.GroupSingle()
sky.add(Sky())

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
                sound_manager.stop_all_music()
                sound_manager.play_music('level1')
            
    if game_active == True:
        prev_time = current_time
        sky.draw(screen)
        screen.blit(ground_surface, (0,GROUND_POS_Y))
        
        pygame.draw.rect(screen, PRIMARY_COLOR, title_background_rect)
        screen.blit(title_text, title_rect)
        current_time = display_score()
        change_bg()
        
        player.draw(screen)
        player.update()
        
        obstacles.draw(screen)
        obstacles.update()
        
        game_active = sprite_collision()
        
    pygame.display.update()
    clock.tick(60)