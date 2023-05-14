import sys
import pygame
from support import import_folder
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, gen_j_particles):
        super().__init__()
        # general attributes
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # Attack animation data
        self.jet_effect = import_folder("data/anim/particles/jet_pistol_effect")
        self.effect_frame_index = 0
        self.effect_animation_speed = 0.3
        self.display_surface = surface

        # particles
        self.gen_j_particles = gen_j_particles
        
        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -16
        self.collision_rect = pygame.Rect(self.rect.topleft, (60, 78))

        # player status
        self.status = "idle"
        self.on_ground = False
        self.on_ceiling = False
        self.facing_right = True
        self.on_left = False
        self.on_right = False

        # attack status
        self.attacking = False
        self.mov_lock = False
        self.cooldown = 1000
    
    def import_character_assets(self):
        character_path = "data/anim/"
        a = "attacks/"
        self.animations = {"idle":[], "run":[], "jump":[], "fall":[], "crouch":[], a+"jet pistol":[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    # Animation method
    def animate(self):
        a = "attacks/"
        animation = self.animations[self.status]

        if self.status == "run":
            self.animation_speed = 0.25
        elif self.status == "fall":
            self.animation_speed = 0.5
        elif self.status == a+"jet pistol":
            self.animation_speed = 0.25
        else: 
            self.animation_speed = 0.1

        # loop frame index
        self.frame_index += self.animation_speed
        if self.frame_index >=  len(animation):
            if not self.status == a+"jet pistol":
                self.frame_index = 0
            elif self.frame_index >= len(animation):
                self.frame_index = len(animation) - 1
                self.attacking = False
                self.mov_lock = False
                self.status = "idle"

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft

        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect.bottomright = self.collision_rect.bottomright

        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

    # Jet pistol effect method
    def j_eff_anim(self):
        if self.attacking:
            self.effect_frame_index += self.effect_animation_speed
            if self.effect_frame_index >= len(self.jet_effect):
                self.effect_frame_index = 0
                
            jet_effect = self.jet_effect[int(self.effect_frame_index)]

            if self.facing_right:
                pos = self.rect.midright - pygame.math.Vector2(0, 50)
                self.display_surface.blit(jet_effect, pos)
            else:
                pos = self.rect.midleft - pygame.math.Vector2(340, 50)
                flip_effect = pygame.transform.flip(jet_effect, True, False)
                self.display_surface.blit(flip_effect, pos)
        

    # KEYBINDS
    def get_input(self):
        a = "attacks/"

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and not self.mov_lock:
            self.direction.x = 1
            self.facing_right = True
    
        elif keys[pygame.K_LEFT] and not self.mov_lock:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        
        if keys[pygame.K_UP] and self.on_ground:
            self.jump()
            self.gen_j_particles(self.rect.midbottom)

            # list = ("data/audio/jump1.wav", "data/audio/jump2.wav")
            # grunt_list = random.choice(list)
            # self.jump_grunt = pygame.mixer.Sound(grunt_list)
            # self.jump_grunt.set_volume(.4)
            # self.jump_grunt.play()
        
        if keys[pygame.K_DOWN] and self.on_ground:
            self.status = "crouch"

        # Jet Pistol
        if keys[pygame.K_s] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if not self.attacking and self.on_ground:
                self.attacking = True
                self.mov_lock = True
                self.attack_start = pygame.time.get_ticks()
                self.status = a+"jet pistol"
                self.j_eff_anim()
        
        # DEBUG  
        if keys[pygame.K_d]:
            print(self.mov_lock, self.attacking, self.status)
            print(self.rect.x, self.rect.y,)
            print("is attacking:", self.attacking)
        
        #TEST
        event_list =pygame.event.get()
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
    
    # Add a cooldown between inputs to prevent input relay every game tick
    def attack_cooldown(self):
        if self.attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_start >= self.cooldown:
                self.attacking = False
                self.mov_lock = False
                self.effect_frame_index = 0
                
    def get_status(self):
        keys = pygame.key.get_pressed()
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            elif not self.attacking and not keys[pygame.K_DOWN]:
                self.status = "idle"
                
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.collision_rect.y += self.direction.y
    
    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.j_eff_anim()
        self.attack_cooldown()