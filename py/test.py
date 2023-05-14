import sys, pygame, random

pygame.init()

clock = pygame.time.Clock()
height = 720
width = 1280
screen = pygame.display.set_mode((width, height))

sound = pygame.mixer.Sound("data/audio/jet-pistol.wav")


while True:
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                sound.play()
            if event.key == pygame.K_s:
                soundlist = ("data/audio/jump1.wav", "data/audio/jump2.wav")
                soundrandom = random.choice(soundlist)
                sound2 = pygame.mixer.Sound(soundrandom)
                sound2.play()
        
            
    screen.fill("#666666")

    pygame.display.update()
    clock.tick(60)