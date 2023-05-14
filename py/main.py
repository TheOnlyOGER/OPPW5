import random
import pygame, sys
from settings import *
from level import Level
from texts import *

pygame.init()
pygame.mixer.init()

# Some lines of code are commented out, which are basically mixer.Sound() code. 
# Running it in this program seems to be highly volatile and risks a lot of crashes.

class Game():
    def __init__(self):
        self.max_health = 100
        self.current_health = 100

        # Music
        self.music_playback = False
        
        self.death_detection = 0
        self.win_detection = 0

        self.won_game = False

        self.level = Level(level_map, screen, self.game_over, self.win)

        self.delay = False
        self.time_delay = 400

    def game_over(self, death_detection):
        self.death_detection += death_detection
        if self.death_detection > 0:
            self.level = Level(level_map, screen, self.game_over, self.win)
            self.death_detection = 0
            # if not self.delay:
            #     self.delay_start = pygame.time.get_ticks()
            #     list = ("data/audio/hit1.wav", "data/audio/hit2.wav", "data/audio/hit3.wav", "data/audio/hit4.wav", "data/audio/hit5.wav")
            #     grunt_list = random.choice(list)
            #     self.dmg = pygame.mixer.Sound(grunt_list)
            #     self.dmg.set_volume(.8)
            #     self.dmg.play()

            #     self.delay = True
        
    def win(self, win_detection):
        self.win_detection += win_detection
        if self.win_detection > 0:
            self.level = Level(level_map, screen, self.game_over, self.win)
            self.won_game = True
            self.win_detection = 0
    
    def delayed_sound(self):
        if self.delay:
            current_time = pygame.time.get_ticks()
            if current_time - self.death_detection >= self.time_delay:
                self.delay = False

    def play_bg_music(self):
        if not self.music_playback:
            self.music = pygame.mixer.music
            self.music.load("data/audio/we-are.ogg")
            self.music.set_volume(0.4)
            self.music.play(loops = -1)
            self.music_playback = True
    
    # Run method
    def run(self):
        if game_active and not self.won_game: # ACTIVE GAME
            self.play_bg_music()
            self.delayed_sound()
            self.level.run()
            ingame_text()
            pygame.mixer.music.unpause()

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                self.level = Level(level_map, screen, self.game_over, self.win)
        
        elif self.won_game: # WIN STATE
            keys = pygame.key.get_pressed()
            pygame.mixer.music.pause()
            win_text_display() 
            self.delayed_sound()

            if keys[pygame.K_RETURN]:
                self.won_game = False

        else: # PAUSED
            pygame.mixer.music.pause()
            paused_text_display() 

# basic setup
pygame.display.set_caption("ONE PIECE PIRATE WARRIORS 5: DEFINITIVE EDITION")
game_active = True
clock = pygame.time.Clock()
icon = pygame.image.load("data/img/mugiwara.png").convert_alpha()
game = Game()

# GAME LOOP
while True:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_active == False:
                    pygame.quit()
                    sys.exit()
                game_active = False

            if event.key == pygame.K_RETURN:
                game_active = True
            
            # if event.key == pygame.K_s:
            #     j_pistol_luffy = pygame.mixer.Sound("data/audio/jet-pistol.wav")
            #     j_pistol_sound = pygame.mixer.Sound("data/audio/jet-pistol-shot.wav")
            #     j_pistol_sound.set_volume(.3)
            #     j_pistol_sound.play(0)
            #     j_pistol_luffy.play(0)

            # Clear Sounds
            if event.key == pygame.K_q:
                pygame.mixer.stop()

    screen.fill("#666666")

    game.run()

    pygame.display.update()
    clock.tick(60)
