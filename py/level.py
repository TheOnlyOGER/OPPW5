import pygame
from tiles import Tile, DeathTile, DestructiveTile, WinTile
from player import Player
from particles import ParticleEffects
from settings import *

class Level:
    def __init__(self, level_data, surface, game_over, win):

        # LEVEL SETUP
        self.display_surface = surface
        self.level_setup(level_data)
        self.world_shift = 0
        self.current_x = 0

        self.game_over = game_over
        self.win = win

        self.destroyed = False

        # DUST
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def gen_j_particles(self, pos):
        pos -= pygame.math.Vector2(0, 40)
        jump_particle_sprite = ParticleEffects(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)
    
    def landing_check(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False
    
    def gen_land_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites(): 
            offset = pygame.math.Vector2(0, 49)
            landing_dust = ParticleEffects(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(landing_dust)
    

    # Applies the level map of the entire game
    def level_setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.wintiles = pygame.sprite.Group()
        self.destructivetiles = pygame.sprite.Group()
        self.deathtiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        # Places specified tiles in accordance to its set letter from settings.py
        for row_index, row in enumerate(layout):
            for col_index, column in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if column == "X":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if column == "W":
                    tile = WinTile((x, y), tile_size)
                    self.wintiles.add(tile)
                if column == "R":
                    tile = DeathTile((x, y), tile_size)
                    self.deathtiles.add(tile)
                if column == "D":
                    tile = DestructiveTile((x, y), tile_size)
                    self.destructivetiles.add(tile)
                if column == "P":
                    player_sprite = Player((x, y), self.display_surface, self.gen_j_particles)
                    self.player.add(player_sprite)

    # Scroll world tiles in relation to player movement
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_X = player.direction.x

        if player_x < width / 3 and direction_X < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > width - (width / 3) and direction_X > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    # HORIZONTAL COLLISION
    def horiz_movement_col(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    self.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right= sprite.rect.left  
                    self.on_right = True
                    self.current_x = player.collision_rect.right
        
        if not self.destroyed:
            for sprite in self.destructivetiles.sprites():
                if sprite.rect.colliderect(player.collision_rect):
                    if player.direction.x < 0:
                        player.collision_rect.left = sprite.rect.right
                        self.on_left = True
                        self.current_x = player.rect.left
                    elif player.direction.x > 0:
                        player.collision_rect.right= sprite.rect.left  
                        self.on_right = True
                        self.current_x = player.collision_rect.right

        

    # VERTICAL COLLISION
    def vert_movement_col(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y  < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if not self.destroyed:
            for sprite in self.destructivetiles.sprites():
                if sprite.rect.colliderect(player.collision_rect):
                    if player.direction.y > 0:
                        player.collision_rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                    elif player.direction.y  < 0:
                        player.collision_rect.top = sprite.rect.bottom
                        player.direction.y = 0
                        player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def tilebreak(self):
        player = self.player.sprite
        keys = pygame.key.get_pressed()
        for sprite in self.destructivetiles.sprites():
            if sprite.rect.colliderect(player.display_surface.get_rect()) and player.facing_right:
                if keys[pygame.K_s]:
                    self.destroyed = True

    def killzone(self):
       player = self.player.sprite
       for sprite in self.deathtiles.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                self.game_over(1)
    
    def winzone(self):
       player = self.player.sprite
       for sprite in self.wintiles.sprites():
            if sprite.rect.colliderect(player.collision_rect):
                self.win(1)


    def run(self):

        self.killzone()
        self.winzone()

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.wintiles.update(self.world_shift)
        self.wintiles.draw(self.display_surface)

        if not self.destroyed:
            self.destructivetiles.update(self.world_shift)
            self.destructivetiles.draw(self.display_surface)

        self.deathtiles.update(self.world_shift)
        self.deathtiles.draw(self.display_surface)
        self.tilebreak()
        self.scroll_x()

        # player
        self.player.update()
        self.horiz_movement_col()
        self.landing_check()
        self.vert_movement_col()
        self.gen_land_dust()
        self.player.draw(self.display_surface)