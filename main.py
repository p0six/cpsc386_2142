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
clock = pygame.time.Clock()
random.seed()


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
        clock.tick(10)  # limits while loop to 10 iterations/second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE and display_help is True:
                    display_help = False
                elif event.key == K_ESCAPE:
                    return False
                elif event.key == K_RETURN:
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
                        computer_opponent = False
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
            rules_img = pygame.image.load('rules.png').convert()
            rules_blit = pygame.transform.scale(rules_img, (800, 600))
            screen.blit(rules_blit, (0, 0))

        # Load background image..
        bg_img = pygame.image.load('menuBackground.png').convert()
        bg_blit = pygame.transform.scale(bg_img, (1024, 768))
        screen.blit(bg_blit, (0, 0))

        # Adding buttons....
        menu_font = pygame.font.Font('Off The Haze.otf', 70)
        start_game_text= menu_font.render('Start Game', True, WHITE)
        start_game_rect = start_game_text.get_rect()  # get rect, byoch!
        start_game_rect.center = ((DISPLAY_WIDTH / 2), 300)
        start_game_button = (start_game_rect.left - 10, start_game_rect.top, (start_game_rect.right + 20) - start_game_rect.left, 30)
        pygame.draw.rect(screen, BLACK, start_game_button)
        screen.blit(start_game_text, start_game_rect)

        # Deal with our menu buttons...
        menu_buttons.clear()
        menu_buttons.append(start_game_button)

        # This must run after all draw commands
        pygame.display.flip()
    return True


def process_play():
    print('process_play')


def draw_game():  # DISPLAY_HEIGHT = 768, img_scroller_one, img_scroller_two
    global img_scroller_one
    global img_scroller_two
    global bg_bool
    bg_img = pygame.image.load('gameBackground.png').convert()
    bg_blit = pygame.transform.scale(bg_img, (1024, 768))
    screen.blit(bg_blit, (0, 0))

    # Need to make this render based on vertical position in img_scroller vars
    gamespace_img_one = pygame.image.load('gamespace1_Test.png').convert()
    gamespace_img_two = pygame.image.load('gamespace2_Test.png').convert()
    gamespace_imgs = [gamespace_img_one, gamespace_img_two]

    gamespace_one_blit = pygame.transform.scale(gamespace_imgs[not bg_bool], (512, 768))
    screen.blit(gamespace_one_blit, (256, img_scroller_one))

    gamespace_two_blit = pygame.transform.scale(gamespace_imgs[bg_bool], (512, 768))
    screen.blit(gamespace_two_blit, (256, img_scroller_one - 768))


    if (img_scroller_one >= 768):
        img_scroller_one = 0
        bg_bool = not bg_bool
    else:
        img_scroller_one += 4

    # cropped = pygame.Surface((512, DISPLAY_HEIGHT))
    # cropped.blit(gamespace_img_one, (0, 0), (0, 0, 512, img_scroller_two))
    # screen.blit(cropped, (256, 0), (0, 0, 512, img_scroller_two))
    img_scroller_two -= 4


    # gamespace_img_two = pygame.image.load('gamespace2_Test.png').convert()
    # gamespace_two_blit = pygame.transform.scale(gamespace_img_two, (512, 768))
    # screen.blit(gamespace_two_blit, (256, 0))

    # This must run after all draw commands
    pygame.display.flip()


def game_loop():
    continue_loop = True  # potentially change until while lines_remaining != nil
    while continue_loop:
        clock.tick(500)  # limits while loop to 10 iterations/second

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False
                elif event.key == K_RETURN: # and len(lines_remaining) == 0:
                    if continue_game is False:
                        return
                    opponent_turn = False
                    boxes.clear()
                    player_score = [0, 0]
                    # lines_remaining = generate_lines()
                    lines_used = []
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