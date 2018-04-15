############################################################################################
#
# Project           : Simple New VG in Pygame
#
# File Name         : 2142.py
#
# Author            : diegofranchi
# CWID              : 889894283
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

pygame.init()

width = 1024
height = 768

black = (0,0,0)
white = (255,255,255)

class PowerUps: #***[1]***
    def __init__(self):
        self.length =
        self.width =
        self.type = 


class Bullet: #***[1]***
    def __init__(self, length=5, width=5, ):
        self.length = 
        self.width = 
        self.area = 
        self.damage =
        self.angle =
        self.speed =
        self.image =

        
class Gun: #***[1]***
    def __init__(self):
        self.type = 
        self.fire_rate =
    
    
class Ship: #***[1]***
    def __init___(self, type):
        self.name = type
        self.setImage()
        self.setGuns()
    def setImage(self):
        if self.name == 'ship_name':
            self.image = pygame.image.load('images/'+self.name)
    def setGuns(self):
        if self.name == 'ship_name':
            self.guns = [Gun(value) for value in range(type)]
        

class Enemy: #***[1]***
    def __init__(self):
        self.type = 
        self.spawn_location = 
        self.angle = 
        self.speed =
        self.hp =


class Player: #***[1]***
    def __init__(self, type):
        self.location = 
        self.ship_image = 
        self.hp = 
    
    
class Game: #***[1]***
    def __init__(self):
        self.level_complete = False
        self.game_loop()
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
        self.draw_game()
    def draw_game(self):
        screen.fill(white)
        pygame.display.update()
        clock.tick(60)


class Menu: #***[1]***
    def __init__(self):
        self.draw_menu()
    def draw_menu(self):
        screen.fill(white)
        pygame.display.update()
        clock.tick(60)
