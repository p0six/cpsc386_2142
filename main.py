#!/usr/bin/env python3
# ######################################################################################################################
# Author: Michael Romero (romerom@csu.fullerton.edu), Diego Franchi (diegofranchi@csu.fullerton.edu)
# CPSC-386 - Intro to Video Game Development
# Project 3: Simple new VG in Pygame
# California State University, Fullerton
# April 17, 2018
# ######################################################################################################################
# TODO: Replace rules.png with rules made for our game...
# TODO: Explosion animation with sprites!
# TODO: Spaceships need health, and we need to be able to adjust it as things get hit.
# TODO: maybe... Check if player score higher than enemy score to determine win condition.
# TODO: Add  a sexy fem audio saying 'Level up'
# TODO: Add PowerUps / Different Weapons with different trajectories, additional bullets, and strength
# DONE: If health runs out... game should end.
# DONE: Health display
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
import math
########################################################################################################################
# Some "constants"
########################################################################################################################
GAME_TITLE = str(2142)
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (240, 250, 250)
DARK_GREY = (90, 90, 50)
WHITE = (255, 255, 255)
########################################################################################################################
# Initialization values..
########################################################################################################################
active_bullets = []
active_enemies = []
active_enemy_bullets = []
active_asteroids = []
player_score = 0
enemy_score = 0
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

points_font = pygame.font.Font('fonts/Off The Haze.otf', 30)
level_font = pygame.font.Font('fonts/Off The Haze.otf', 90)
########################################################################################################################


class Enemy:
    def __init__(self, enemy_img, target):
        self.image_file = enemy_img
        self.image = pygame.image.load(enemy_img).convert_alpha()
        self.rect = self.image.get_rect()
        self.health = 3
        self.min_speed = 1
        self.max_speed = 6
        self.x_increasing = True if random.getrandbits(1) else False
        self.velocity_x = random.randint(self.min_speed, self.max_speed - 1) if self.x_increasing \
            else random.randint(self.min_speed, self.max_speed - 1) * -1
        self.velocity_y = random.randint(self.min_speed + 1, self.max_speed)  # always want this value a positive...
        self.x, self.y = (random.randint(0, 512 - self.rect.width), 0 - self.rect.height)
        self.location = self.x, self.y
        self.target_x, self.target_y = target
        self.target = target
        self.active_bullets = []
        self.weapon_charge = 0
        self.degrees_rotated = 0

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (self.x + self.rect.width / 2, self.y - 3*self.rect.height/4)

    def next_location(self, target):
        self.target = target
        self.target_x, self.target_y = target
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
        self.set_location(self.x + self.velocity_x, self.y + self.velocity_y)
        self.rotate(target)
        return self.x, self.y

    def rotate(self, target):
        self.image = pygame.image.load(self.image_file).convert_alpha()
        if self.y - self.target_y < 0:
            self.degrees_rotated = math.degrees(math.atan((self.x - self.target_x) / (self.y - self.target_y)))
        else:
            self.degrees_rotated = math.degrees(math.atan((self.x - self.target_x) / (self.y - self.target_y))) + 180
        self.image = pygame.transform.rotate(self.image, self.degrees_rotated).convert_alpha()

    def fire(self, image):
        if self.weapon_charge >= 25:
            my_bullet = EnemyBullet(image, (self.x + self.rect.width / 2, self.y + self.rect.height / 2), self.target)
            self.active_bullets.append(my_bullet)
            self.weapon_charge = 0
            return my_bullet
        else:
            self.weapon_charge += 1
        return None


class EnemyBullet:
    def __init__(self, bullet_img, location, target):
        self.image_file = bullet_img
        self.image = pygame.image.load(bullet_img).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180).convert_alpha()
        self.rect = self.image.get_rect()
        self.location = location
        self.target_x, self.target_y = target
        self.damage = 1
        self.speed = 8
        self.x, self.y = self.location
        self.rect.center = (self.x + self.rect.width / 2, self.y - 3*self.rect.height/4)
        vel_x, vel_y = self.x - self.target_x, self.y - self.target_y
        self.vector = pygame.math.Vector2(vel_x, vel_y).normalize()
        self.vector.scale_to_length(self.speed)
        self.velocity_x, self.velocity_y = self.vector
        self.degrees_rotated = 0
        self.rotate()

    def rotate(self):
        if self.y == player_blue.y:
            self.y += 1
        self.image = pygame.image.load(self.image_file).convert_alpha()
        if self.y - self.target_y < 0:
            self.degrees_rotated = math.degrees(math.atan((self.x - self.target_x) / (self.y - self.target_y)))
        else:
            self.degrees_rotated = math.degrees(math.atan((self.x - self.target_x) / (self.y - self.target_y))) + 180
        self.image = pygame.transform.rotate(self.image, self.degrees_rotated).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180).convert_alpha()

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.location = (self.x, self.y)
        self.rect.center = (self.x + self.rect.width / 2, self.y - 3*self.rect.height/4)

    def next_location(self):
        if (self.velocity_x <= 0 and self.x + self.velocity_x + 2*self.rect.height <= 0) \
                        or (self.velocity_x >= 0 and self.x + self.velocity_x - 2*self.rect.height >= 512):
            if self in active_enemy_bullets:
                active_enemy_bullets.remove(self)
            return -400, -400
        if (self.velocity_y <= 0 and self.y + self.velocity_y + 2*self.rect.height <= 0) \
                or (self.velocity_y >= 0 and self.y + self.velocity_y - 2*self.rect.height >= 768):
            if self in active_enemy_bullets:
                active_enemy_bullets.remove(self)
            return -400, -400
        self.set_location(self.x - self.velocity_x, self.y - self.velocity_y)
        return self.x, self.y


class Bullet:
    def __init__(self, bullet_img, location, degrees_rotated):
        self.image_file = bullet_img
        self.image = pygame.image.load(bullet_img).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180).convert_alpha()
        # self.degrees_rotated = player_blue.degrees_rotated
        self.degrees_rotated = degrees_rotated
        self.rect = self.image.get_rect()
        self.location = location
        self.damage = 1
        self.speed = 24
        self.x, self.y = self.location
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.mouse_x -= 256
        vel_x, vel_y = self.x - self.mouse_x, self.y - self.mouse_y
        self.vector = pygame.math.Vector2(vel_x, vel_y).normalize()
        self.vector.scale_to_length(self.speed)
        self.velocity_x, self.velocity_y = self.vector
        self.rotate()
        bullet_sound.play()

    def set_location(self, x, y):
        self.x = x
        self.y = y
        self.location = (self.x, self.y)
        self.rect.center = (self.x + self.rect.width / 2, self.y - 3*self.rect.height/4)

    def rotate(self):
        if self.y == self.mouse_y:
            self.mouse_y += 1
        self.image = pygame.image.load(self.image_file).convert_alpha()
        if self.y - self.mouse_y < 0:
            self.degrees_rotated = math.degrees(math.atan((self.x - self.mouse_x) / (self.y - self.mouse_y)))
        else:
            self.degrees_rotated = math.degrees(math.atan((self.x - self.mouse_x) / (self.y - self.mouse_y))) + 180
        self.image = pygame.transform.rotate(self.image, self.degrees_rotated).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180).convert_alpha()

    def next_location(self):
        if (self.velocity_x <= 0 and self.x + self.velocity_x + 2*self.rect.height <= 0) \
                or (self.velocity_x >= 0 and self.x + self.velocity_x - 2*self.rect.height >= 512):
            if self in active_enemy_bullets:
                active_enemy_bullets.remove(self)
            return -400, -400
        if (self.velocity_y <= 0 and self.y + self.velocity_y + 2*self.rect.height <= 0) \
                or (self.velocity_y >= 0 and self.y + self.velocity_y - 2*self.rect.height >= 768):
            if self in active_enemy_bullets:
                active_enemy_bullets.remove(self)
            return -400, -400
        self.set_location(self.x - self.velocity_x, self.y - self.velocity_y)
        return self.x, self.y


class Player:
    def __init__(self, ship_image, target):
        self.image = pygame.image.load(ship_image).convert_alpha()
        self.image_file = ship_image
        self.rect = self.image.get_rect()
        self.location = ((DISPLAY_WIDTH / 2) / 2 - (self.rect.width / 2), (DISPLAY_HEIGHT - (self.rect.height * 1.5)))
        self.x, self.y = self.location
        self.rect.center = (self.x + self.rect.width / 2, self.y - self.rect.height / 2)
        self.mouse_x, self.mouse_y = target
        self.mouse_x -= 256
        self.target = target
        self.speed = 8
        self.hp = 20
        self.degrees_rotated = 0
        self.rotate(self.target)

    def rotate(self, target):
        self.image = pygame.image.load(self.image_file).convert_alpha()
        self.mouse_x, self.mouse_y = target
        self.mouse_x -= 256
        if self.y - self.mouse_y < 0:
            self.degrees_rotated = math.degrees(math.atan((self.x - self.mouse_x) / (self.y - self.mouse_y))) + 180
        else:
            self.degrees_rotated = math.degrees(math.atan((self.x - self.mouse_x) / (self.y - self.mouse_y)))
        self.image = pygame.transform.rotate(self.image, self.degrees_rotated).convert_alpha()

    def fire(self, image):
        return Bullet(image, (self.x + self.rect.width / 2, self.y + self.rect.height / 2), self.degrees_rotated)

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


def evaluate_menu_click(event, menu_buttons):  # rectangle's: (top left x, top left y, width, height)
    x, y = event.pos
    for button in menu_buttons:
        if button[0] <= x <= button[0] + button[2] and button[1] <= y <= button[1] + button[3]:
            return button
    return None


def game_menu():
    global player_score, enemy_score, display_help
    pygame.mixer.music.load('sounds/menu_audio_01.ogg')
    pygame.mixer.music.set_volume(0.232)
    pygame.mixer.music.play(-1, 0)
    menu_buttons = []
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
                    new_game()
                    return True
                elif event.key == pygame.K_h:
                    display_help = True
            elif event.type == pygame.MOUSEBUTTONDOWN:  # on diego's laptop, this is right click for some reason
                button_clicked = evaluate_menu_click(event, menu_buttons)
                if button_clicked is not None:
                    index = menu_buttons.index(button_clicked)
                    if index == 0:  # first button starts game, exits menu..
                        new_game()
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


def new_game():
    global player_score, enemy_score, player_blue, level
    active_enemy_bullets.clear()
    active_bullets.clear()
    active_enemies.clear()
    player_score = enemy_score = 0
    level = 1
    player_blue = Player('images/SpaceShooterRedux/PNG/playerShip1_blue.png', pygame.mouse.get_pos())


def draw_game():  # DISPLAY_HEIGHT = 768, img_scroller_one, img_scroller_two
    global img_scroller_one, bg_bool, player_score, level, enemy_score, score_changed

    screen.blit(game_bg_blit, (0, 0))

    # Points display..
    points_text = points_font.render(str(player_score), True, WHITE)
    points_text_rect = points_text.get_rect()  # get rect, byoch!
    points_text_rect.left = 22
    points_text_rect.top = 45
    screen.blit(points_text, points_text_rect)

    enemy_points_text = points_font.render(str(enemy_score), True, WHITE)
    enemy_points_text_rect = enemy_points_text.get_rect()  # get rect, byoch!
    enemy_points_text_rect.right = 990
    enemy_points_text_rect.top = 45
    screen.blit(enemy_points_text, enemy_points_text_rect)

    # This is our neverending scrolling background....
    scroller_bg = pygame.Surface((512, 768))

    scroller_bg.blit(gamespace_img_blits[not bg_bool], (0, img_scroller_one))
    scroller_bg.blit(gamespace_img_blits[bg_bool], (0, img_scroller_one - DISPLAY_HEIGHT))

    # Display a health bar...
    if player_blue.hp > 0:
        pygame.draw.rect(screen, RED, (22, 700, player_blue.hp * 10, 40))

    # Display our current level...
    level_text = level_font.render(str(level), True, WHITE)
    level_text_rect = level_text.get_rect()  # get rect, byoch!
    level_text_rect.right = 900
    level_text_rect.top = 600
    screen.blit(level_text, level_text_rect)

    #  Display bullets...
    for bullet in active_bullets:
        scroller_bg.blit(bullet.image, bullet.location)
        bullet.next_location()
        for active_enemy in active_enemies:
            if bullet.rect.colliderect(active_enemy.rect):
                explosion_enemy.play()
                player_score += 1
                score_changed = True
                if bullet in active_bullets and active_enemy in active_enemies:
                    active_bullets.remove(bullet)
                    active_enemies.remove(active_enemy)
                    continue
        if bullet not in active_bullets:
            continue

    # Display ship on top of bullet to create effect that bullet comes out of ship
    scroller_bg.blit(player_blue.image, player_blue.location)

    for enemy in active_enemies:
        scroller_bg.blit(enemy.image, enemy.next_location(player_blue.location))
        if enemy.rect.colliderect(player_blue.rect):
            explosion_player.play()
            player_blue.hp = 0
        for enemy_bullet in enemy.active_bullets:
            if enemy_bullet.rect.colliderect(player_blue.rect):
                explosion_player.play()
                enemy_score += 1
                player_blue.hp -= (enemy_bullet.damage if player_blue.hp >= 1 else 0)
                if enemy_bullet in enemy.active_bullets:
                    enemy.active_bullets.remove(enemy_bullet)
            scroller_bg.blit(enemy_bullet.image, enemy_bullet.location)
            enemy_bullet.next_location()

    # remaining shots that belong to dead enemy
    for enemy_bullet in active_enemy_bullets:
        if enemy_bullet.rect.colliderect(player_blue.rect):
            explosion_player.play()
            enemy_score += 1
            player_blue.hp -= (enemy_bullet.damage if player_blue.hp >= 1 else 0)
            if enemy_bullet in active_enemy_bullets:
                active_enemy_bullets.remove(enemy_bullet)
        scroller_bg.blit(enemy_bullet.image, enemy_bullet.location)
        enemy_bullet.next_location()

    # Paint our scrolling background...
    screen.blit(scroller_bg, (256, 0))

    # Slow this puppy down..
    clock.tick(30)  # 30 FPS Max

    # This must run after all draw commands
    pygame.display.flip()

    # We can use this to scroll two images together infinitely...
    if img_scroller_one >= DISPLAY_HEIGHT:
        img_scroller_one = 0
        bg_bool = not bg_bool
    else:
        img_scroller_one += 2  # controls how fast our background scrolls by..


def game_loop():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('sounds/oakenfold.ogg')
    pygame.mixer.music.set_volume(0.232)
    pygame.mixer.music.play(-1, 105.2)
    global level, score_changed
    score_changed = False
    level = 1

    continue_loop = True
    while continue_loop:
        # Direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if keys[pygame.K_a]:
                player_blue.up_left()
            elif keys[pygame.K_d]:
                player_blue.up_right()
            else:
                player_blue.up()
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if keys[pygame.K_a]:
                player_blue.down_left()
            elif keys[pygame.K_d]:
                player_blue.down_right()
            else:
                player_blue.down()
        elif keys[pygame.K_a]:
            player_blue.left()
        elif keys[pygame.K_d]:
            player_blue.right()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                active_bullets.append(player_blue.fire('images/SpaceShooterRedux/PNG/Lasers/laserBlue01.png'))
                for enemy in active_enemies:
                    enemy.weapon_charge += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.fadeout(4)
                    pygame.mixer.music.stop()
                    return False
                elif event.key == pygame.K_SPACE:
                    active_bullets.append(player_blue.fire('images/SpaceShooterRedux/PNG/Lasers/laserBlue01.png'))
                    for enemy in active_enemies:
                        enemy.weapon_charge += 1

        # Ensure the player is always rotated towards the direction of the mouse cursor...
        player_blue.rotate(pygame.mouse.get_pos())

        # Increase the amount of enemies on the screen every 10 points..
        if score_changed and player_score >= 10 and player_score % 10 == 0:
            level += 1
            score_changed = False

        if len(active_enemies) < 2 + level:
            active_enemies.append(Enemy('images/SpaceShooterRedux/PNG/Enemies/enemyBlack1.png', player_blue.location))

        for enemy in active_enemies:
            enemy_bullet = enemy.fire('images/SpaceShooterRedux/PNG/Lasers/laserRed01.png')
            if enemy_bullet is not None:
                active_enemy_bullets.append(enemy_bullet)
        draw_game()

        if player_blue.hp == 0:
            pygame.mixer.music.stop()
            continue_loop = game_over() # TODO: This is where to add the game over screen.


def game_over():
    # Reused game_menu logic to create new buttons and headers
    menu_buttons = []
    clock.tick(5)  # 5 FPS while in Game Menu..
    menu_font = pygame.font.Font('fonts/Off The Haze.otf', 70)
    game_over_text = menu_font.render('GAME OVER', True, WHITE)
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = ((DISPLAY_WIDTH / 2), 200)
    play_again_text = menu_font.render('Play Again?', True, WHITE)
    play_again_text_rect = play_again_text.get_rect()  # get rect, byoch!
    play_again_text_rect.center = ((DISPLAY_WIDTH / 2), 400)
    play_again_button = (play_again_text_rect.left - 10, play_again_text_rect.top - 10,
                         (play_again_text_rect.right + 10) - (play_again_text_rect.left - 10),
                         (play_again_text_rect.bottom + 10) - (play_again_text_rect.top - 10))
    menu_buttons.append(play_again_button)
    quit_text = menu_font.render('       Quit', True, WHITE)
    quit_text_rect = game_over_text.get_rect()
    quit_text_rect.center = ((DISPLAY_WIDTH / 2), 600)
    quit_button = (quit_text_rect.left - 10, quit_text_rect.top - 10,
                         (quit_text_rect.right + 10) - (quit_text_rect.left - 10),
                         (quit_text_rect.bottom + 10) - (quit_text_rect.top - 10))
    menu_buttons.append(quit_button)
    display_help = False

    # load image here to prevent the rabbit from floating around backwards
    rabbit_img = pygame.image.load("images/space_rabbit.png")
    rabbit_blit = pygame.transform.scale(rabbit_img, (177, 286))
    rabbit_rect = rabbit_blit.get_rect()
    speed = [5, 5]
    while True:
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
                    new_game()
                    pygame.mixer.music.load('sounds/oakenfold.ogg')
                    pygame.mixer.music.set_volume(0.232)
                    pygame.mixer.music.play(-1, 105.2)
                    return True
                elif event.key == pygame.K_h:
                    display_help = True
            elif event.type == pygame.MOUSEBUTTONDOWN:  # on diego's laptop, this is right click for some reason
                button_clicked = evaluate_menu_click(event, menu_buttons)
                if button_clicked is not None:
                    index = menu_buttons.index(button_clicked)
                    if index == 0:  # first button starts game, exits menu..
                        new_game()
                        pygame.mixer.music.load('sounds/oakenfold.ogg')
                        pygame.mixer.music.set_volume(0.232)
                        pygame.mixer.music.play(-1, 105.2)
                        return True
                    else:
                        return False

        screen.blit(game_bg_blit, (0, 0))
        screen.blit(gamespace_one_blit, (256, 0))
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(play_again_text, play_again_text_rect)
        screen.blit(quit_text, quit_text_rect)

        # bouncy bunny boing boing
        rabbit_rect = rabbit_rect.move(speed)
        if rabbit_rect.left < 0 or rabbit_rect.right > DISPLAY_WIDTH:
            speed[0] = -speed[0]
            rabbit_blit = pygame.transform.flip(rabbit_blit, True, False)
        if rabbit_rect.top < 0 or rabbit_rect.bottom > DISPLAY_HEIGHT:
            speed[1] = -speed[1]
        screen.blit(rabbit_blit, rabbit_rect)

        # Draw help if requested..
        if display_help is True:
            screen.blit(rules_blit, (0, 0))

        # This must run after all draw commands
        pygame.display.flip()


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
