#!/usr/bin/env python3
# ######################################################################################################################
# Author: Michael Romero (romerom@csu.fullerton.edu), Diego Franchi (diegofranchi@csu.fullerton.edu)
# CPSC-386 - Intro to Video Game Development
# Project 3: Simple new VG in Pygame
# California State University, Fullerton
# April 17, 2018
# ######################################################################################################################
# TODO: Spaceships need health, and we need to be able to adjust it as things get hit. also display health..
# TODO: If health runs out... game should end.
# TODO: Explosion animation with sprites!
# TODO: Add PowerUps / Different Weapons with different vectors, additional bullets, and strength
# TODO: add a bunny!
# ######################################################################################################################
# Sprites via Kenney @ https://opengameart.org/content/space-shooter-redux
# ######################################################################################################################
# Description:
# Pygame throwback to old 2d shooters like 1942, Raiden, etc.
#
# Add a bunny:
# Powerups are in the form of bunnies
# ######################################################################################################################
import random
import pygame
# from pygame.locals import *

########################################################################################################################
# Some "constants"
########################################################################################################################
GAME_TITLE = str(2148)
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # unused thus far.. could potentially add 2 or more opponents
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (240, 250, 250)
DARK_GREY = (90, 90, 50)
WHITE = (255, 255, 255)
########################################################################################################################
# Initialization values..
########################################################################################################################
menu_buttons = []
active_bullets = []
active_enemies = []
active_enemy_bullets = []
active_asteroids = []
player_score = 0
img_scroller_one = 0
bg_bool = True
########################################################################################################################
pygame.init()
pygame.display.set_caption(GAME_TITLE)  # title of the window...
screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_HEIGHT])
clock = pygame.time.Clock()
random.seed()

bullet_sound = pygame.mixer.Sound('sounds/sfx_laser2.ogg')
explosion_enemy = pygame.mixer.Sound('sounds/explosion_enemy.wav')
explosion_player = pygame.mixer.Sound('sounds/explosion_player.wav')
bullet_sound.play()
########################################################################################################################


class Enemy:
    def __init__(self, enemy_img):
        self.image = pygame.image.load(enemy_img).convert_alpha()
        self.rect = self.image.get_rect()
        self.damage = 1
        self.health = 3
        self.min_speed = 1
        self.max_speed = 6
        self.x_increasing = True if random.getrandbits(1) else False
        self.velocity_x = random.randint(self.min_speed, self.max_speed - 1) if self.x_increasing \
            else random.randint(self.min_speed, self.max_speed - 1) * -1
        self.velocity_y = random.randint(self.min_speed + 1, self.max_speed)  # always want this value a positive...
        self.x, self.y = (random.randint(0, 512 - self.rect.width), 0 - self.rect.height)
        self.active_bullets = []

    def set_location(self, x, y):
        self.x = x
        self.y = y

    def next_location(self):
        if (self.velocity_x < 0 and self.x + self.velocity_x <= 0 - self.rect.width) \
                or (self.velocity_x > 0 and self.x + self.velocity_x >= 512):
            if self in active_enemies:
                active_enemies.remove(self)
            return -200, -200
        elif (self.velocity_y < 0 and self.y + self.velocity_y <= 0) \
                or (self.velocity_y > 0 and self.y + self.velocity_y >= 768):
            if self in active_enemies:
                active_enemies.remove(self)
            return -200, -200
        self.rect.center = (self.x + self.rect.width / 2, self.y - 3*self.rect.height/4)
        self.set_location(self.x + self.velocity_x, self.y + self.velocity_y)
        return self.x, self.y

    def fire(self, image):
        my_bullet = EnemyBullet(image, (self.x + self.rect.width / 2, self.y + self.rect.height / 2),
                                (self.velocity_x, self.velocity_y), self.x_increasing)
        self.active_bullets.append(my_bullet)
        return my_bullet


class EnemyBullet:
    def __init__(self, bullet_img, location, vector, x_increasing):
        self.image = pygame.image.load(bullet_img).convert_alpha()
        self.rect = self.image.get_rect()
        self.location = location
        self.x, self.y = self.location
        self.velocity_x, self.velocity_y = vector
        self.x_increasing = x_increasing
        self.speed = 8

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.location = (self.x, self.y)
        self.rect.center = (self.x + self.rect.width / 2, self.y - 3*self.rect.height/4)

    def next_location(self):
        if self.y - self.speed + self.rect.height < 0:
            if self in active_bullets:
                active_bullets.remove(self)
            return -200, -200
        self.set_location(self.x, self.y + self.speed)
        return self.x, self.y + self.speed

    def next_vector_location(self):
        if (self.velocity_x < 0 and self.x + self.velocity_x <= 0 - self.rect.width) \
                or (self.velocity_x > 0 and self.x + self.velocity_x >= 512):
            if self in active_enemy_bullets:
                active_enemy_bullets.remove(self)
            return -200, -200
        elif (self.velocity_y < 0 and self.y + self.velocity_y <= 0) \
                or (self.velocity_y > 0 and self.y + self.velocity_y >= 768):
            if self in active_enemy_bullets:
                active_enemy_bullets.remove(self)
            return -200, -200
        self.set_location((self.x + self.velocity_x + self.speed * (1 if self.x_increasing else -1)),
                          self.y + self.velocity_y + self.speed)
        return self.location


class Bullet:
    def __init__(self, bullet_img, location):
        self.image = pygame.image.load(bullet_img).convert_alpha()
        self.rect = self.image.get_rect()
        self.location = location
        self.x, self.y = self.location
        self.damage = 1
        self.angle = 1
        self.speed = 24
        bullet_sound.play()

    def set_location(self, x, y):
        self.location = (self.x, self.y)
        self.x = x
        self.y = y
        self.rect.center = (self.x + self.rect.width / 2, self.y - self.rect.height)

    def next_location(self):
        if self.y - self.speed + self.rect.height < 0:
            if self in active_bullets:
                active_bullets.remove(self)
            return -200, -200
        self.set_location(self.x, self.y - self.speed)
        return self.location


class Player:
    def __init__(self, ship_image):
        self.image = pygame.image.load(ship_image).convert_alpha()
        self.rect = self.image.get_rect()
        self.location = ((DISPLAY_WIDTH / 2) / 2 - (self.rect.width / 2), (DISPLAY_HEIGHT - (self.rect.height * 1.5)))
        self.x, self.y = self.location
        self.rect.center = self.location
        self.speed = 8
        self.hp = 100

    def fire(self, image):
        return Bullet(image, (self.x + self.rect.width / 2, self.y - self.rect.height / 2))

    def set_location(self, x, y):
        if x < 0 or x > 512 - self.rect.width or y < 0 or y > DISPLAY_HEIGHT - self.rect.height:
            return
        self.x = x
        self.y = y
        self.location = (self.x, self.y)
        self.rect.center = (self.x + self.rect.width / 2, self.y - self.rect.height / 2)

    def up(self):
        self.set_location(self.x, self.y - self.speed)

    def down(self):
        self.set_location(self.x, self.y + self.speed)

    def left(self):
        self.set_location(self.x - self.speed, self.y)

    def right(self):
        self.set_location(self.x + self.speed, self.y)

    def up_left(self):
        self.set_location(self.x - self.speed, self.y - self.speed)

    def up_right(self):
        self.set_location(self.x + self.speed, self.y - self.speed)

    def down_left(self):
        self.set_location(self.x - self.speed, self.y + self.speed)

    def down_right(self):
        self.set_location(self.x + self.speed, self.y + self.speed)


########################################################################################################################
# Do some things once, and never again, in order to save CPU time.
########################################################################################################################
rules_img = pygame.image.load('images/rules.png').convert()
rules_blit = pygame.transform.scale(rules_img, (800, 600)).convert()
menu_bg_img = pygame.image.load('images/menuBackground.png').convert()
menu_bg_blit = pygame.transform.scale(menu_bg_img, (1024, 768)).convert()
game_bg_img = pygame.image.load('images/gameBackground.png').convert()
game_bg_blit = pygame.transform.scale(game_bg_img, (1024, 768)).convert()

# Can use two different background images and they'll infinitely follow eachother... for now, use same image
gamespace_img_one = pygame.image.load('images/space_background.png').convert()
gamespace_img_two = pygame.image.load('images/space_background.png').convert()
gamespace_one_blit = pygame.transform.scale(gamespace_img_one, (512, 768)).convert()
gamespace_two_blit = pygame.transform.scale(gamespace_img_two, (512, 768)).convert()
gamespace_img_blits = [gamespace_one_blit, gamespace_two_blit]

points_font = pygame.font.Font('fonts/Off The Haze.otf', 35)
player_blue = Player('images/SpaceShooterRedux/PNG/playerShip1_blue.png')
########################################################################################################################
# Audio
########################################################################################################################
pygame.mixer.music.load('sounds/oakenfold.ogg')
pygame.mixer.music.set_volume(0.232)
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
    menu_font = pygame.font.Font('fonts/Off The Haze.otf', 70)
    start_game_text = menu_font.render('Start Game', True, WHITE)
    start_game_text_rect = start_game_text.get_rect()  # get rect, byoch!
    start_game_text_rect.center = ((DISPLAY_WIDTH / 2), 300)
    start_game_button = (start_game_text_rect.left - 10, start_game_text_rect.top - 10,
                         (start_game_text_rect.right + 10) - (start_game_text_rect.left - 10),
                         (start_game_text_rect.bottom + 10) - (start_game_text_rect.top - 10))
    menu_buttons.append(start_game_button)
    display_help = False
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if display_help is True:
                        display_help = False
                    else:
                        return False
                elif event.key == pygame.K_RETURN:  # should reset all game values here...
                    player_score = 0
                    return True
                elif event.key == pygame.K_h:
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


def draw_game():  # DISPLAY_HEIGHT = 768, img_scroller_one, img_scroller_two
    global img_scroller_one
    global bg_bool
    global player_score

    screen.blit(game_bg_blit, (0, 0))

    # Points display..
    points_text = points_font.render(str(player_score), True, WHITE)
    points_text_rect = points_text.get_rect()  # get rect, byoch!
    points_text_rect.left = 28
    points_text_rect.top = 60
    screen.blit(points_text, points_text_rect)

    # This is our neverending scrolling background....
    scroller_bg = pygame.Surface((512, 768))

    scroller_bg.blit(gamespace_img_blits[not bg_bool], (0, img_scroller_one))
    scroller_bg.blit(gamespace_img_blits[bg_bool], (0, img_scroller_one - DISPLAY_HEIGHT))

    # Our player...
    scroller_bg.blit(player_blue.image, player_blue.location)

    # ...who fires bullets...
    for bullet in active_bullets:
        for active_enemy in active_enemies:
            if bullet.rect.colliderect(active_enemy.rect) and bullet in active_bullets:
                explosion_enemy.play()
                active_bullets.remove(bullet)
                if active_enemy in active_enemies:  # bullet actually collides many times... remove only once.
                    active_enemies.remove(active_enemy)
                player_score += 1
            else:
                scroller_bg.blit(bullet.image, bullet.location)
        bullet.next_location()

    # ...has enemies...
    for enemy in active_enemies:
        scroller_bg.blit(enemy.image, enemy.next_location())
        if enemy.rect.colliderect(player_blue.rect):
            explosion_player.play()

        # ...that also fire bullets...
        for enemy_bullet in enemy.active_bullets:
            enemy_bullet.next_location()
            if enemy_bullet.rect.colliderect(player_blue.rect):
                explosion_player.play()
                if enemy_bullet in enemy.active_bullets:
                    enemy.active_bullets.remove(enemy_bullet)
            scroller_bg.blit(enemy_bullet.image, enemy_bullet.location)

    # ...which do not disappear merely because the enemy has died.
    for enemy_bullet in active_enemy_bullets:
        enemy_bullet.next_location()
        if enemy_bullet.rect.colliderect(player_blue.rect):
            explosion_player.play()
            if enemy_bullet in active_enemy_bullets:
                active_enemy_bullets.remove(enemy_bullet)
        scroller_bg.blit(enemy_bullet.image, enemy_bullet.location)

    # Paint our scrolling background...
    screen.blit(scroller_bg, (256, 0))

    # This must run after all draw commands
    pygame.display.flip()

    # We can use this to scroll two images together infinitely...
    if img_scroller_one >= DISPLAY_HEIGHT:
        img_scroller_one = 0
        bg_bool = not bg_bool
    else:
        img_scroller_one += 2  # controls how fast our background scrolls by..


def game_loop():
    pygame.mixer.music.play(-1, 105.2)
    clock.tick(30)  # 30 FPS Max

    continue_loop = True  # potentially change until while lines_remaining != nil
    while continue_loop:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_blue.up_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_blue.up_right()
            else:
                player_blue.up()
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_blue.down_left()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_blue.down_right()
            else:
                player_blue.down()
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_blue.left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_blue.right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.fadeout(4)
                    pygame.mixer.music.stop()
                    return False
                elif event.key == pygame.K_SPACE:
                    active_bullets.append(player_blue.fire('images/SpaceShooterRedux/PNG/Lasers/laserBlue01.png'))
                    for enemy in active_enemies:
                        active_enemy_bullets.append(enemy.fire('images/SpaceShooterRedux/PNG/Lasers/laserBlue01.png'))
        if len(active_enemies) < 3:
            active_enemies.append(Enemy('images/SpaceShooterRedux/PNG/Enemies/enemyBlack1.png'))

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
