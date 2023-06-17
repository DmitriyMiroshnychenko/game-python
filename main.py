import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, MOUSEBUTTONDOWN

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 700
WIDTH = 1200

FONT = pygame.font.SysFont('Arial', 30)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_ORANGE = (255, 165, 0)
COLOR_GREEN = (0, 255, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect(center=(WIDTH/2, HEIGHT/2))
player_move_down = [0, 4]
player_move_up = [0, -4]
player_move_right = [4, 0]
player_move_left = [-4, 0]


def create_enemy():
    enemy_size = (20, 20)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(enemy_size[1], HEIGHT - enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]


def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(0, WIDTH - bonus.get_width()), 0, *bonus.get_size())
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1000)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0

image_index = 0

game_over = False


def draw_play_again_button():
    button_text = FONT.render("Играть заново", True, COLOR_BLACK)
    button_rect = button_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    pygame.draw.rect(main_display, COLOR_GREEN, button_rect.inflate(20, 10))
    main_display.blit(button_text, button_rect)


def check_play_again_button():
    mouse_pos = pygame.mouse.get_pos()
    button_rect = FONT.render("Играть заново", True, COLOR_BLACK).get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    if button_rect.collidepoint(mouse_pos):
        return True
    return False


while not game_over:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True

        if event.type == CREATE_ENEMY and len(enemies) < 5:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS and len(bonuses) < 3:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

        if event.type == MOUSEBUTTONDOWN and game_over:
            if check_play_again_button():
                # Reset game variables
                enemies = []
                bonuses = []
                score = 0
                image_index = 0
                game_over = False

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]) or enemy[1].top < 0 or enemy[1].bottom > HEIGHT:
            game_over = True

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top < 0:
            bonuses.pop(bonuses.index(bonus))

    if game_over:
        draw_play_again_button()

pygame.display.flip()
