import pygame
from sys import exit
from random import randint, choice

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SKY_WIDTH = 800
SKY_HEIGHT = 300
GROUND_POS_Y = 300
FLY_POS_Y = 200
PLAYER_POS_X = 100
GAME_NAME = "Jumper Game"
OBSTACLE_SPEED = 5
GRAVITY = 0.3
JUMP_HEIGHT = 30
PRIMARY_COLOR = '#8bcfba'
LEVEL_CHANGE = 100

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
        
        self.jump_sound = pygame.mixer.Sound('./tutorial/assets/audios/jump.mp3')
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

class SoundManager():
    def __init__(self):
        pygame.mixer.init()
        self.musics = {
            'start' : pygame.mixer.Sound('./tutorial/assets/audios/title.wav'),
            'level1' : pygame.mixer.Sound('./tutorial/assets/audios/level1.wav'),
            'level2' : pygame.mixer.Sound('./tutorial/assets/audios/level2.wav'),
            'level3' : pygame.mixer.Sound('./tutorial/assets/audios/level3.wav'),
            'ending' : pygame.mixer.Sound('./tutorial/assets/audios/ending.wav'),
        }
        
    def play_music(self, music_name):
        self.musics[music_name].set_volume(0.1)
        self.musics[music_name].play(loops=-1)
        
    def stop_all_music(self):
        for music in self.musics:
            self.musics[music].stop()

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