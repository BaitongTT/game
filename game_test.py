import os
import random
import math
import pygame
from pygame_button import button
from os import listdir
from os.path import isfile, join
pygame.init()

#framerate
clock = pygame.time.Clock()
FPS = 140

#
playyer_1 = 3
start_game = False

pygame.display.set_caption('Trick or Treat' )
screen = pygame.display.set_mode((720, 400))
width, length = screen.get_size() #get the windows size
#print(width, length) to get 1536, 864
screen.fill((0, 0, 0))

background_1 = pygame.image.load("Image/background_2.png").convert_alpha()
background_rect_1 = background_1.get_rect()
Block = pygame.image.load("Image/block.png").convert_alpha()
Block_rect = Block.get_rect()

run = True
while run:
    clock.tick(FPS)
    
    ##Startgame
    
    if start_game == False :
        background_start = pygame.image.load("Image/background_1.png").convert_alpha()
        background_rect_start = background_start.get_rect()
        screen.blit(background_start,background_rect_start)
        #button start
        pass
        
    else:
        screen.blit(background_1,background_rect_1)
        screen.blit(Block,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.display.update()
pygame.quit()
