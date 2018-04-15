#!/usr/bin/env python3
# ######################################################################################################################
# Author: Michael Romero / romerom@csu.fullerton.edu
# CPSC-386 - Intro to Video Game Development
# Project 2: Simple Classic Video Game in Pygame
# California State University, Fullerton
# March 23, 2018
# ######################################################################################################################
# DONE: 60% for playable game
# DONE: 10% for a clearly defined win and lose state
# DONE: 10% for a legal and random Brain opponent
# DONE: 10% for online instructions or tutoring
# DONE: 5% for a reasonable README.txt file
# DONE: 5% for following the Submission rules
# ######################################################################################################################
# TODO: Add some keys to allow player to create new game / restart game
# TODO: Play a sound when game is over?
# TODO: Maybe give players the option of choosing a color
# TODO: Boxes to represent punches / kicks to opponents bunny avatar, SF2 with an energy bar based on lines_remaining
# ######################################################################################################################
# Description:
# The dots and boxes game, as described here: https://en.wikipedia.org/wiki/Dots_and_Boxes
#
# Add a bunny:
# For each box, there is 1/8 chance the box will include a bunny, awarding 4 points for each box with a bunny.
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
continue_game = True
img_scroller_one = 0
img_scroller_two = 768
bg_bool = True
########################################################################################################################
# Initialization values..
########################################################################################################################
boxes = []
menu_buttons = []
########################################################################################################################

pygame.init()

pygame.display.set_caption(GAME_TITLE)  # title of the window...
screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])
# clock = pygame.time.Clock()
random.seed()

# Performance change: manipulate images here so they only need to be loaded once.
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
menu_font = pygame.font.Font('fonts/Off The Haze.otf', 70)
start_game_text= menu_font.render('Start Game', True, WHITE)
start_game_text_rect = start_game_text.get_rect()  # get rect, byoch!
start_game_text_rect.center = ((DISPLAY_WIDTH / 2), 300)
start_game_button = (start_game_text_rect.left - 10, start_game_text_rect.top - 10,
                     (start_game_text_rect.right + 10) - (start_game_text_rect.left - 10),
                     (start_game_text_rect.bottom + 10) - (start_game_text_rect.top - 10))
menu_buttons.append(start_game_button)


def evaluate_menu_click(event):  # rectangle's: (top left x, top left y, width, height)
    x, y = event.pos
    for button in menu_buttons:
        if button[0] <= x <= button[0] + button[2] and button[1] <= y <= button[1] + button[3]:
            return button
    return None


def game_menu():
    global COLS
    global ROWS
    global computer_opponent
    global opponent_turn
    global boxes
    global player_score
    global display_help
    intro = True
    while intro:
        # clock.tick(30)  # limits while loop to 30 iterations/second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE and display_help is True:
                    display_help = False
                elif event.key == K_ESCAPE:
                    return False
                elif event.key == K_RETURN: # should reset all game values here...
                    opponent_turn = False
                    boxes.clear()
                    player_score = [0, 0]
                    return True
                elif event.key == K_h:
                    display_help = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_clicked = evaluate_menu_click(event)
                if button_clicked is not None:
                    index = menu_buttons.index(button_clicked)
                    if index == 0:
                        # computer_opponent = False
                        return True
                    elif index == 1:
                        computer_opponent = True
                    elif index == 2:
                        COLS = ROWS = 5
                    elif index == 3:
                        COLS = ROWS = 7
                    else:
                        COLS = ROWS = 9

        # Draw help if requested..
        if display_help is True:
            screen.blit(rules_blit, (0, 0))
        else: # Load background image..
            screen.blit(menu_bg_blit, (0, 0))

        pygame.draw.rect(screen, BLACK, start_game_button)
        screen.blit(start_game_text, start_game_text_rect)

        # Deal with our menu buttons...

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
    pygame.mixer.music.play(-1, 154.055)
    screen.blit(game_bg_blit, (0, 0))

    continue_loop = True  # potentially change until while lines_remaining != nil
    while continue_loop:
        # clock.tick(30)  # limits while loop to 30 frames/second
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
                # elif event.key == K_RETURN: # and len(lines_remaining) == 0:
                #     if continue_game is False:
                #         return
                    #opponent_turn = False
                    #boxes.clear()
                    #player_score = [0, 0]
                    # lines_remaining = generate_lines()
                    #lines_used = []
                    computer_opponent = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                print('mouse down')
                # if len(lines_remaining) == 0:
                #     continue_button = evaluate_continue_click(event)
                #     if continue_button is not None:
                #         index = continue_buttons.index(continue_button)
                #         if index == 0:
                #             continue_game = False
                #         else:
                #             continue_game = True
                # else:
                #     evaluate_click(event, lines_remaining, lines_used)

        # draw_game(lines_remaining, lines_used)
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