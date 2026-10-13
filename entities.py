import math
import random
import pygame

from settings import (
    WIDTH, PLAY_HEIGHT, DARK_GREEN, BLUE, RED, BLACK,
    WHITE, GREEN1, GREEN2, TILE
)

from maze import blocked


def spawn_zombie(zombies, player):
    for _ in range(200):
        side = random.randrange(4)

        if side == 0:
            pos = pygame.Vector2(
                random.randint(25, WIDTH - 25), 25
            )

        elif side == 1:
            pos = pygame.Vector2(
                random.randint(25, WIDTH - 25),
                PLAY_HEIGHT - 25
            )

        elif side == 2:
            pos = pygame.Vector2(
                25, random.randint(25, PLAY_HEIGHT - 25)
            )

        else:
            pos = pygame.Vector2(
                WIDTH - 25,
                random.randint(25, PLAY_HEIGHT - 25)
            )

        if not blocked(pos, 14) and pos.distance_to(player) > 180:
            zombies.append(pos)
            return


def spawn_medkit(medkits, player):
    for _ in range(200):
        pos = pygame.Vector2(
            random.randint(30, WIDTH - 30),
            random.randint(30, PLAY_HEIGHT - 30),
        )

        if not blocked(pos, 12) and pos.distance_to(player) > 45:
            medkits.append(pos)
            return


def draw_floor(screen):
    for y in range(0, PLAY_HEIGHT, TILE):
        for x in range(0, WIDTH, TILE):
            if (x // TILE + y // TILE) % 2 == 0:
                color = GREEN1
            else:
                color = GREEN2

            pygame.draw.rect(
                screen, color, (x, y, TILE, TILE)
            )

            pygame.draw.line(
                screen,
                (48, 130, 55),
                (x, y + TILE - 2),
                (x + TILE, y + TILE - 2),
                1,
            )


def draw_player(screen, player):
    mouse = pygame.Vector2(pygame.mouse.get_pos())
    direction = mouse - player

    if direction.length_squared() > 0:
        direction = direction.normalize()

    pygame.draw.ellipse(
        screen,
        DARK_GREEN,
        (
            int(player.x - 15),
            int(player.y + 8),
            30,
            12,
        ),
    )

    pygame.draw.circle(
        screen,
        BLUE,
        (int(player.x), int(player.y + 3)),
        13,
    )

    pygame.draw.rect(
        screen,
        (110, 70, 35),
        (
            int(player.x - 12),
            int(player.y - 5),
            8,
            14,
        ),
        border_radius=3,
    )

    pygame.draw.circle(
        screen,
        (235, 185, 135),
        (int(player.x), int(player.y - 9)),
        8,
    )

    pygame.draw.arc(
        screen,
        (40, 40, 35),
        (
            int(player.x - 8),
            int(player.y - 17),
            16,
            12,
        ),
        0,
        math.pi,
        4,
    )

    gun_start = player + direction * 7
    gun_end = player + direction * 24

    pygame.draw.line(
        screen,
        (35, 35, 35),
        (int(gun_start.x), int(gun_start.y)),
        (int(gun_end.x), int(gun_end.y)),
        6,
    )


def draw_zombie(screen, zombie):
    x, y = int(zombie.x), int(zombie.y)

    pygame.draw.ellipse(
        screen, DARK_GREEN, (x - 15, y + 8, 30, 10)
    )

    pygame.draw.line(
        screen, (90, 145, 55),
        (x - 8, y), (x - 19, y + 8), 6
    )

    pygame.draw.line(
        screen, (90, 145, 55),
        (x + 8, y), (x + 19, y + 8), 6
    )

    pygame.draw.rect(
        screen, (85, 100, 45),
        (x - 11, y - 5, 22, 22),
        border_radius=5
    )

    pygame.draw.circle(
        screen, (120, 170, 65), (x, y - 10), 11
    )

    pygame.draw.circle(
        screen, (45, 55, 35), (x - 7, y - 17), 5
    )

    pygame.draw.circle(
        screen, (45, 55, 35), (x + 3, y - 20), 5
    )

    pygame.draw.circle(
        screen, RED, (x - 4, y - 11), 2
    )

    pygame.draw.circle(
        screen, RED, (x + 4, y - 11), 2
    )

    pygame.draw.line(
        screen, BLACK, (x - 4, y - 4), (x + 4, y - 4), 2
    )


def draw_medkit(screen, pos):
    x, y = int(pos.x), int(pos.y)

    pygame.draw.circle(screen, WHITE, (x, y), 13)

    pygame.draw.rect(
        screen, RED, (x - 3, y - 8, 6, 16)
    )

    pygame.draw.rect(
        screen, RED, (x - 8, y - 3, 16, 6)
    )