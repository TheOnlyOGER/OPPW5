import pygame
from settings import *

def paused_text_display():
    # fonts
    title_font = pygame.font.Font("data/font/MinecraftTen-VGORe.ttf", 50)
    font = pygame.font.Font("data/font/Minecraft.otf", 20)

    # pause text
    pause = title_font.render("GAME PAUSED", False, "White")
    pause_rect = pause.get_rect(center = (width/2, height/2))

    continuetext = font.render("Press enter to continue...", False, "White")
    continuetext_rect = continuetext.get_rect(center = (width/2, height/1.75))

    esctext = font.render("ESC again to close the game", False, "White")
    esctext_rect = esctext.get_rect(center = (width/2, height/1.6))

    screen.blit(pause, pause_rect)
    screen.blit(continuetext, continuetext_rect)
    screen.blit(esctext, esctext_rect)

def win_text_display():
    # fonts
    title_font = pygame.font.Font("data/font/MinecraftTen-VGORe.ttf", 50)

    # pause text
    win = title_font.render("YOU WIN!!!", False, "White")
    win_rect = win.get_rect(center = (width/2, height/2))

    screen.fill("Green")
    screen.blit(win, win_rect)

def ingame_text():
    # fonts
    font = pygame.font.Font("data/font/Minecraft.otf", 20)

    # Version
    version = font.render("Version 0.1c: Most stable build, zero risk crashing", False, "White")
    version_rect = version.get_rect(midleft = (20, 20))

    # pause
    pause = font.render("ESC to Pause", False, "White")
    pause_rect = pause.get_rect(midleft = (20, 50))

    # movement
    movement = font.render("Arrow keys to move", False, "White")
    movement_rect = movement.get_rect(midleft = (20, 80))
    
    # crouch
    crouch = font.render("Down arrow to crouch", False, "White")
    crouch_rect = crouch.get_rect(midleft = (20, 110))

    # guide text
    guide = font.render('S to use "Gum Gum: Jet Pistol"', False, "White")
    guide_rect = guide.get_rect(midleft = (20, 140))

    screen.blit(version, version_rect)
    screen.blit(pause, pause_rect)
    screen.blit(movement, movement_rect)
    screen.blit(crouch, crouch_rect)    
    screen.blit(guide, guide_rect)