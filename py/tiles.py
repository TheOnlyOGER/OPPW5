import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.surface.Surface((size, size))
        self.image.fill("grey")
        self.rect = self.image.get_rect(topleft = pos)
    
    # Scroll screen to left or right
    def update(self, x_shift):
        self.rect.x += x_shift

# Different types of tiles
class WinTile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.surface.Surface((size, size))
        self.image.fill("green")
        self.rect = self.image.get_rect(topleft = pos)
    
    # Scroll screen to left or right
    def update(self, x_shift):
        self.rect.x += x_shift

class DestructiveTile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.surface.Surface((size, size))
        self.image.fill("Yellow")
        self.rect = self.image.get_rect(topleft = pos)
    
    # Scroll screen to left or right
    def update(self, x_shift):
        self.rect.x += x_shift

class DeathTile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.surface.Surface((size, size))
        self.image.fill("Red")
        self.rect = self.image.get_rect(topleft = pos)
    
    # Scroll screen to left or right
    def update(self, x_shift):
        self.rect.x += x_shift