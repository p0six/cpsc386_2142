#!/usr/bin/env python3
# ######################################################################################################################
# Author: Michael Romero (romerom@csu.fullerton.edu), Diego Franchi (diegofranchi@csu.fullerton.edu)
# CPSC-386 - Intro to Video Game Development
# Project 3: Simple new VG in Pygame
# California State University, Fullerton
# April 17, 2018
# ######################################################################################################################
# TODO: Finish classes for each game asset type, including functions that determine next position of each
# TODO: Finish logic which manipulates each of the classes when creating a game... determining when to add to game board
# ######################################################################################################################
# Description:
# Pygame throwback to old 2d shooters like 1942, Raiden, etc.
#
# Add a bunny:
# Powerups are in the form of bunnies
# ######################################################################################################################
import random
import pygame
import sys
import math
from pygame.locals import *

########################################################################################################################
# Some "constants"
########################################################################################################################
GAME_TITLE = '2148'
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # unused thus far.. could potentially add 2 or more opponents
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (240, 250, 250)
DARK_GREY = (90, 90, 50)
WHITE = (255, 255, 255)
display_help = False
player_score = 0
continue_game = True
img_scroller_one = 0
bg_bool = True
########################################################################################################################
# Initialization values..
########################################################################################################################
menu_buttons = []
########################################################################################################################

pygame.init()
pygame.display.set_caption(GAME_TITLE)  # title of the window...
screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])
clock = pygame.time.Clock()
random.seed()

########################################################################################################################
# Do some things once, and never again, in order to save CPU time.
########################################################################################################################
rules_img = pygame.image.load('images/rules.png').convert()
rules_blit = pygame.transform.scale(rules_img, (800, 600))
menu_bg_img = pygame.image.load('images/menuBackground.png').convert()
menu_bg_blit = pygame.transform.scale(menu_bg_img, (1024, 768))
game_bg_img = pygame.image.load('images/gameBackground.png').convert()
game_bg_blit = pygame.transform.scale(game_bg_img, (1024, 768))
gamespace_img_one = pygame.image.load('images/gamespace1_Test.png').convert()
gamespace_one_blit = pygame.transform.scale(gamespace_img_one, (512, 768))
gamespace_img_two = pygame.image.load('images/gamespace2_Test.png').convert()
gamespace_two_blit = pygame.transform.scale(gamespace_img_two, (512, 768))
gamespace_img_blits = [gamespace_one_blit, gamespace_two_blit]
pygame.mixer.music.load('sounds/oakenfold.ogg')
pygame.mixer.music.set_volume(0.232)

# I hate PyGame buttons...
menu_font = pygame.font.Font('fonts/Off The Haze.otf', 70)
start_game_text= menu_font.render('Start Game', True, WHITE)
start_game_text_rect = start_game_text.get_rect()  # get rect, byoch!
start_game_text_rect.center = ((DISPLAY_WIDTH / 2), 300)
start_game_button = (start_game_text_rect.left - 10, start_game_text_rect.top - 10,
                     (start_game_text_rect.right + 10) - (start_game_text_rect.left - 10),
                     (start_game_text_rect.bottom + 10) - (start_game_text_rect.top - 10))
menu_buttons.append(start_game_button)
########################################################################################################################


def evaluate_menu_click(event):  # rectangle's: (top left x, top left y, width, height)
    x, y = event.pos
    for button in menu_buttons:
        if button[0] <= x <= button[0] + button[2] and button[1] <= y <= button[1] + button[3]:
            return button
    return None


def game_menu():
    global player_score
    global display_help
    clock.tick(5)  # 5 FPS while in Game Menu..
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if display_help is True:
                        display_help = False
                    else:
                        return False
                elif event.key == K_RETURN: # should reset all game values here...
                    player_score = 0
                    return True
                elif event.key == K_h:
                    display_help = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = evaluate_menu_click(event)
                if button_clicked is not None:
                    index = menu_buttons.index(button_clicked)
                    if index == 0:  # first button starts game, exits menu..
                        player_score = 0
                        return True

        screen.blit(menu_bg_blit, (0, 0))
        pygame.draw.rect(screen, BLACK, start_game_button)
        screen.blit(start_game_text, start_game_text_rect)

        # Draw help if requested..
        if display_help is True:
            screen.blit(rules_blit, (0, 0))

        # This must run after all draw commands
        pygame.display.flip()
    return True


def process_play():
    print('process_play')


def draw_game():  # DISPLAY_HEIGHT = 768, img_scroller_one, img_scroller_two
    global img_scroller_one
    global bg_bool

    # Need to make this render based on vertical position in img_scroller vars
    screen.blit(gamespace_img_blits[not bg_bool], (256, img_scroller_one))
    screen.blit(gamespace_img_blits[bg_bool], (256, img_scroller_one - DISPLAY_HEIGHT))

    # This must run after all draw commands
    pygame.display.flip()

    if img_scroller_one >= DISPLAY_HEIGHT:
        img_scroller_one = 0
        bg_bool = not bg_bool
    else:
        img_scroller_one += 4


def game_loop():
    pygame.mixer.music.play(-1, 105.2)
    screen.blit(game_bg_blit, (0, 0))
    clock.tick(30)  # 30 FPS Max

    continue_loop = True  # potentially change until while lines_remaining != nil
    while continue_loop:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            print('up is held')
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                print('left is also held')
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                print('right is also held')
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            print('down is held')
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                print('left is also held')
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                print('right is also held')
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            print('left is held')
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            print('right is held')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mixer.music.fadeout(4)
                    pygame.mixer.music.stop()
                    return False

        draw_game()


def main():
    continue_loop = True
    while continue_loop:
        continue_loop = game_menu()
        if continue_loop:
            game_loop()
    pygame.quit()
    exit()


if __name__ == '__main__':
    main()