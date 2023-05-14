from os import walk
import pygame

'''
Function which allows the game to more easily import all files in a specified folder when specified inside of the parameter.
Using the walk method to relay the full file names and its directory to then list all files inside folder via a for loop and sorting it to list every file numerically.
This will ensure that every frame of an animation is arranged in its proper order. In order to display it correctly.
'''
def import_folder(path):
    surf_list = []

    for _, __, img_files in walk(path):
        for image in sorted(img_files, key = lambda x: '{0:0>8}'. format(x)):
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surf_list.append(image_surf)
    
    return surf_list

# debugging the function, irrelevant to the full code
def debug(path):
    surf_list = []
    for _, __, img_files in walk(path):
        for image in sorted(img_files, key=lambda x: '{0:0>8}'.format(x)):
            #print(image)
            pass
    return surf_list

# test any animation in x folder
debug("data/anim/attacks/jet pistol")
