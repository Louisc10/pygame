import pygame
from sys import exit
from random import randint

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

def init():
    screen.blit(sky_surface, (0,0))
    screen.blit(ground_surface, (0,GROUND_POS_Y))
    pygame.draw.rect(screen, '#8bcfba', title_background_rect)
    screen.blit(title_text, title_rect)
    screen.blit(start_text, start_rect)

def display_score(screen, start_time):
    current_time = (int)((pygame.time.get_ticks()- start_time)/1000)
    score_text = font.render(f'Score: { current_time }', True, PRIMARY_COLOR)
    score_rect = score_text.get_rect(center = (SCREEN_WIDTH/2, 60))
    screen.blit(score_text, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle_rect, obstacle_type, obstacle_index = obstacle[0], obstacle[1], obstacle[2]
            obstacle_rect.x -= OBSTACLE_SPEED
            if obstacle_rect.right < 0:
                obstacle_list.remove(obstacle)
            if(obstacle_type == 0):
                screen.blit(snail[int(obstacle_index)], obstacle_rect)
            else:
                screen.blit(fly[int(obstacle_index)], obstacle_rect)
                
    return obstacle_list

def obstacle_animation(obstacle_list): 
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle_type, obstacle_index = obstacle[1], obstacle[2]
            obstacle_index += 0.1
            if(obstacle_type == 0):
                if obstacle_index >= len(snail):
                    obstacle_index = 0
            else:
                if obstacle_index >= len(fly):
                    obstacle_index = 0
            obstacle[2] = obstacle_index
    return obstacle_list

def obstacle_collision(obstacle_list):
    game_active = True
    if obstacle_list:
        for obstacle in obstacle_list:            
            if obstacle[0].colliderect(player_rect):
                print("You Lose!")
                game_active = False
                screen.blit(lose_text, lose_rect)
                screen.blit(start_text, start_rect)
    return game_active

def player_animation():
    global player_rect, player_index, player_walk, player_jump_surface
    if player_rect.bottom == GROUND_POS_Y:
        screen.blit(player_walk[int(player_index)], player_rect)
        player_index += 0.1
    else:
        screen.blit(player_jump_surface, player_rect)
    if player_index >= len(player_walk):
        player_index = 0
    return player_index

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

#obstacles
snail_1_surface = pygame.image.load('./tutorial/assets/images/snail/snail1.png').convert_alpha()
snail_2_surface = pygame.image.load('./tutorial/assets/images/snail/snail2.png').convert_alpha()
snail = [snail_1_surface, snail_2_surface] #0

fly_1_surface = pygame.image.load('./tutorial/assets/images/fly/fly1.png').convert_alpha()
fly_2_surface = pygame.image.load('./tutorial/assets/images/fly/fly2.png').convert_alpha()
fly = [fly_1_surface, fly_2_surface] #1

obstacle_list = []

#player
player_jump_surface = pygame.image.load('./tutorial/assets/images/player/jump.png').convert_alpha()
player_walk_1_surface = pygame.image.load('./tutorial/assets/images/player/player_walk_1.png').convert_alpha()
player_walk_2_surface = pygame.image.load('./tutorial/assets/images/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1_surface, player_walk_2_surface]
player_index = 0
player_rect = player_walk_1_surface.get_rect(bottomleft = (PLAYER_POS_X, GROUND_POS_Y))
player_gravity = 0

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

init()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if  game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == GROUND_POS_Y:
                    player_gravity -= GRAVITY * JUMP_HEIGHT
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                    
            if event.type == obstacle_timer:
                print("Create Obstacle!")
                type = randint(0, 1)
                if type == 0:
                    obstacle_list.append([snail_1_surface.get_rect(bottomleft = (randint(SCREEN_WIDTH, SCREEN_WIDTH + 200), GROUND_POS_Y)), type, 0])
                else:
                    obstacle_list.append([fly_1_surface.get_rect(bottomleft = (randint(SCREEN_WIDTH, SCREEN_WIDTH + 200), FLY_POS_Y)), type, 0])
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                player_gravity = 0
                player_rect.bottom = GROUND_POS_Y
                start_time = pygame.time.get_ticks()
                init()
                obstacle_list.clear()
            
    if game_active == True:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,GROUND_POS_Y))
        
        pygame.draw.rect(screen, PRIMARY_COLOR, title_background_rect)
        screen.blit(title_text, title_rect)
        display_score(screen, start_time)
        
        player_gravity += GRAVITY
        player_rect.y += player_gravity
        if(player_rect.bottom >= GROUND_POS_Y): 
            player_rect.bottom = GROUND_POS_Y
            player_gravity = 0
            
        player_index = player_animation()
        
        obstacle_list = obstacle_movement(obstacle_list)
        game_active = obstacle_collision(obstacle_list)
        
        obstacle_list = obstacle_animation(obstacle_list)
    pygame.display.update()
    clock.tick(60)