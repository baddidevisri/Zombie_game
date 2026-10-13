import math
import pygame

from settings import *
from maze import blocked, move_safely, draw_walls
from entities import (
    spawn_zombie, spawn_medkit, draw_floor, draw_player,
    draw_zombie, draw_medkit
)
from ui import draw_centered, draw_button, draw_hud

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Apocalypse - Survival Maze")

# Load the game icon from the same folder.
try:
    icon = pygame.image.load("game_icon.png")
    pygame.display.set_icon(icon)
except (pygame.error, FileNotFoundError):
    pass

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 22, bold=True)
small_font = pygame.font.SysFont("arial", 16, bold=True)
title_font = pygame.font.SysFont("arial", 42, bold=True)
medium_font = pygame.font.SysFont("arial", 28, bold=True)

fonts = (font, small_font, medium_font)

game_state = MENU
level = 1
score = 0
health = 100
kills = 0
level_target = 5
time_left = LEVEL_TIME
last_damage = 0

player = pygame.Vector2(70, 70)

bullets = []
zombies = []
medkits = []

pause_button = pygame.Rect(
    720, PLAY_HEIGHT + 42, 160, 38
)


def start_level():
    global player, kills, level_target
    global time_left, last_damage, game_state

    player = pygame.Vector2(70, 70)

    bullets.clear()
    zombies.clear()
    medkits.clear()

    kills = 0
    level_target = 5 + (level - 1) * 3
    time_left = LEVEL_TIME

    last_damage = pygame.time.get_ticks()

    zombie_count = min(4 + level, 10)

    for _ in range(zombie_count):
        spawn_zombie(zombies, player)

    for _ in range(2):
        spawn_medkit(medkits, player)

    game_state = PLAYING


def restart_game():
    global level, score, health

    level = 1
    score = 0
    health = 100

    start_level()


def draw_overlay(alpha=200):
    overlay = pygame.Surface(
        (WIDTH, HEIGHT), pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, alpha))
    screen.blit(overlay, (0, 0))


def draw_game_scene():
    draw_floor(screen)

    draw_walls(screen, WALL, WALL_LIGHT)

    for kit in medkits:
        draw_medkit(screen, kit)

    for bullet in bullets:
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(bullet[0].x), int(bullet[0].y)),
            5,
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (int(bullet[0].x), int(bullet[0].y)),
            2,
        )

    for zombie in zombies:
        draw_zombie(screen, zombie)

    draw_player(screen, player)

    return draw_hud(
        screen, health, score, level, MAX_LEVEL,
        time_left, kills, level_target, fonts
    )


running = True

while running:
    dt = clock.tick(60) / 1000.0
    now = pygame.time.get_ticks()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if game_state == MENU:
                start_button = pygame.Rect(
                    WIDTH // 2 - 130, 390, 260, 60
                )

                if (
                    event.button == 1
                    and start_button.collidepoint(mouse_pos)
                ):
                    restart_game()

            elif event.button == 1:

                if pause_button.collidepoint(mouse_pos):

                    if game_state == PLAYING:
                        game_state = PAUSED

                    elif game_state == PAUSED:
                        game_state = PLAYING

                elif game_state == PLAYING:

                    direction = (
                        pygame.Vector2(mouse_pos) - player
                    )

                    if direction.length_squared() > 0:
                        direction = direction.normalize()
                        start = player + direction * 20

                        bullets.append([
                            start,
                            direction * BULLET_SPEED
                        ])

            if (
                game_state in (GAME_OVER, VICTORY)
                and event.button == 1
            ):
                button_y = (
                    440 if game_state == GAME_OVER else 480
                )

                restart_button = pygame.Rect(
                    WIDTH // 2 - 130,
                    button_y,
                    260,
                    60,
                )

                if restart_button.collidepoint(mouse_pos):
                    restart_game()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_q:
                running = False

            if game_state == MENU:

                if event.key == pygame.K_RETURN:
                    restart_game()

            elif game_state == PLAYING:

                if event.key in (
                    pygame.K_p, pygame.K_ESCAPE
                ):
                    game_state = PAUSED

            elif game_state == PAUSED:

                if event.key in (
                    pygame.K_p,
                    pygame.K_ESCAPE,
                    pygame.K_RETURN,
                ):
                    game_state = PLAYING

            elif (
                game_state == LEVEL_COMPLETE
                and event.key == pygame.K_RETURN
            ):

                if level < MAX_LEVEL:
                    level += 1
                    start_level()
                else:
                    game_state = VICTORY

            elif (
                game_state in (GAME_OVER, VICTORY)
                and event.key == pygame.K_r
            ):
                restart_game()

    # Update gameplay
    if game_state == PLAYING:

        time_left -= dt

        if time_left <= 0:
            time_left = 0
            game_state = GAME_OVER

        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0, 0)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1

        if move.length_squared() > 0:
            move = move.normalize() * PLAYER_SPEED
            move_safely(player, move)

        # Move bullets
        for bullet in bullets[:]:
            bullet[0] += bullet[1]

            if (
                bullet[0].x < 0
                or bullet[0].x > WIDTH
                or bullet[0].y < 0
                or bullet[0].y > PLAY_HEIGHT
                or blocked(bullet[0], 3)
            ):
                bullets.remove(bullet)

        # Move zombies and check collisions
        for zombie in zombies[:]:

            direction = player - zombie

            if direction.length_squared() > 0:
                direction = direction.normalize()

                zombie_speed = 1.0 + (
                    (level - 1) * 0.2
                )

                move_safely(
                    zombie,
                    direction * zombie_speed,
                    12,
                )

            if (
                zombie.distance_to(player) < 25
                and now - last_damage > 500
            ):
                health -= 5
                last_damage = now

                knockback = zombie - player

                if knockback.length_squared() > 0:
                    knockback = knockback.normalize()

                    move_safely(
                        zombie, knockback * 18, 12
                    )

            for bullet in bullets[:]:

                if zombie.distance_to(bullet[0]) < 20:

                    if zombie in zombies:
                        zombies.remove(zombie)

                    if bullet in bullets:
                        bullets.remove(bullet)

                    score += 10
                    kills += 1

                    if kills < level_target:
                        spawn_zombie(zombies, player)

                    break

        # Collect medkits
        for kit in medkits[:]:

            if player.distance_to(kit) < 25:
                health = min(100, health + 25)
                medkits.remove(kit)

                spawn_medkit(medkits, player)

        if kills >= level_target:
            game_state = LEVEL_COMPLETE

        if health <= 0:
            health = 0
            game_state = GAME_OVER

    # Draw the game
    pause_button = draw_game_scene()

    if game_state == MENU:
        draw_overlay(210)

        draw_centered(
            screen, "ZOMBIE APOCALYPSE",
            title_font, RED, 150
        )

        draw_centered(
            screen, "SURVIVAL MAZE",
            medium_font, GREEN, 215
        )

        draw_centered(
            screen,
            "Survive the maze. Eliminate the zombies!",
            font, WHITE, 275
        )

        draw_centered(
            screen,
            "Complete all 5 levels before time runs out.",
            small_font, WHITE, 320
        )

        start_button = pygame.Rect(
            WIDTH // 2 - 130, 390, 260, 60
        )

        draw_button(
            screen, "START GAME",
            start_button, (30, 135, 65), medium_font
        )

        draw_centered(
            screen, "WASD / ARROWS: MOVE",
            small_font, WHITE, 490
        )

        draw_centered(
            screen, "MOUSE CLICK: SHOOT   |   P: PAUSE",
            small_font, WHITE, 520
        )

        draw_centered(
            screen, "Press ENTER to start",
            small_font, YELLOW, 565
        )

    elif game_state == PAUSED:
        draw_overlay(190)

        draw_centered(
            screen, "GAME PAUSED",
            title_font, YELLOW, 230
        )

        draw_centered(
            screen, "Take a break!",
            medium_font, WHITE, 300
        )

        draw_centered(
            screen, "Press P / ESC / ENTER to Resume",
            font, GREEN, 365
        )

        draw_centered(
            screen, "Press Q to Quit",
            small_font, WHITE, 415
        )

    elif game_state == LEVEL_COMPLETE:
        draw_overlay(195)

        draw_centered(
            screen, f"LEVEL {level} COMPLETED!",
            title_font, GREEN, 230
        )

        draw_centered(
            screen, f"Score: {score}",
            medium_font, YELLOW, 300
        )

        if level < MAX_LEVEL:
            draw_centered(
                screen, "Get ready for the next challenge!",
                font, WHITE, 355
            )

            draw_centered(
                screen, "Press ENTER to continue",
                font, GREEN, 415
            )

        else:
            draw_centered(
                screen, "All levels completed!",
                font, WHITE, 355
            )

            draw_centered(
                screen, "Press ENTER to see your victory",
                font, GREEN, 415
            )

    elif game_state == GAME_OVER:
        draw_overlay(210)

        draw_centered(
            screen, "GAME OVER",
            title_font, RED, 230
        )

        draw_centered(
            screen, "You could not survive!",
            medium_font, WHITE, 295
        )

        draw_centered(
            screen, f"Final Score: {score}",
            font, YELLOW, 350
        )

        draw_centered(
            screen, "Press R to Restart",
            font, GREEN, 400
        )

        restart_button = pygame.Rect(
            WIDTH // 2 - 130, 440, 260, 60
        )

        draw_button(
            screen, "PLAY AGAIN",
            restart_button, (35, 125, 60), medium_font
        )

    elif game_state == VICTORY:
        draw_overlay(210)

        draw_centered(
            screen, "YOU SURVIVED!",
            title_font, GREEN, 220
        )

        draw_centered(
            screen, "CONGRATULATIONS!",
            medium_font, YELLOW, 290
        )

        draw_centered(
            screen, "You completed all 5 levels!",
            font, WHITE, 345
        )

        draw_centered(
            screen, f"FINAL SCORE: {score}",
            font, YELLOW, 390
        )

        draw_centered(
            screen, "Press R to Play Again",
            font, GREEN, 435
        )

        restart_button = pygame.Rect(
            WIDTH // 2 - 130, 480, 260, 60
        )

        draw_button(
            screen, "PLAY AGAIN",
            restart_button, (35, 125, 60), medium_font
        )

    pygame.display.flip()

pygame.quit()