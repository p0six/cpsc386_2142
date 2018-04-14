############################################################################################
#
# Project           : Simple New VG in Pygame
#
# Program Name      : 2142.py
#
# Author            : diegofranchi, mikeromero
# CWID              : 889894283, 
#
# Date Created      : 20180413
#
# Purpose           : design, prototype, and build a new (simple) video game in Python + Pygame
#
# Revision History  :
#
# Date        Author        Ref     Revision (Date in YYYMMDD format)
# 20180413   diegofranchi   1       Created game skeleton with classes + variables 
#
############################################################################################

import pygame
import time
from random import shuffle

pygame.init()
pygame.mixer.init()

width = 1024
height = 768

black = (0,0,0)
white = (255,255,255)


# def text_objects(text, font):
    # textSurface = font.render(text, True, black)
    # return textSurface, textSurface.get_rect()

    
    
class Power_Ups: #***[1]***
    def __init__(self):
        self.type = 


class Bullet: #***[1]***
    def __init__(self):
        self.length = 
        self.width = 
        self.area = 
        self.damange = 
        self.direction = 
        self.speed =
        self.img = 

        
class Gun: #***[1]***
    def __init__(self):
        self.type = 
        self.rate = 
    
    
class Ship: #***[1]***
    def __init___(self, numGun):
        self.type =
        self.image =
        self.guns = [Gun(value) for value in range(numGun)]
      
        

class Enemy: #***[1]***
    def __init__(self):
        self.type = 
        self.spawn_location = 
        self.angle = 
        self.speed =
        self.hp = 
    def __len__(self):
        



class Player: #***[1]***
    def __init__(self, type):
        self.location = 
        self.ship_image = 
        self.hp = 
    
    
class Game: #***[1]***
    def __init__(self):
        self.level_complete = False
    def game_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                
    def draw_game(self):
        
    
    
class Menu: #***[1]***
    def __init__(self):
        self.draw_menu()
    def draw_menu(self):
        screen.fill(white)
        python.display.update()
        clock.tick(60)


def main(): #***[1]***
    Menu()


if __name__ == "__main__": #***[1]***
    main()
