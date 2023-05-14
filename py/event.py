import pygame

# Special binds — just wanted to test if this method worked or not
def event_bind(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_a:
            print("A")
 

