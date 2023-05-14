import pygame

level_map = [
'R',
'R       P                     D  ',
'R     XXX      X              D ',
'R                     XXX     D    ',
'R                             D                X',
'R X             X           XXX      XX    X',
'R X            XX      XX   XXX  X                X                     XXXXXXW',
'R             X        XX  X      XX    X                     X    X',
'R      XXXXXXXX     XX  XXXXX                        XXXX',
'R  XXXXXX  XXXXX    XX  XXXXXX',
'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR',
]

tile_size = 64
width = 1280
height = len(level_map) * tile_size

screen = pygame.display.set_mode((width, height))