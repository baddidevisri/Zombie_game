import pygame

from settings import (
    WIDTH, HEIGHT, PLAY_HEIGHT, DARK, GREEN, WHITE,
    RED, YELLOW
)


def draw_text(screen, text, font_object, color, x, y):
    image = font_object.render(text, True, color)
    screen.blit(image, (x, y))


def draw_centered(screen, text, font_object, color, y):
    image = font_object.render(text, True, color)

    screen.blit(
        image,
        (WIDTH // 2 - image.get_width() // 2, y)
    )


def draw_button(screen, text, rect, color, medium_font):
    pygame.draw.rect(
        screen, color, rect, border_radius=10
    )

    pygame.draw.rect(
        screen, WHITE, rect, 2, border_radius=10
    )

    image = medium_font.render(text, True, WHITE)

    screen.blit(
        image,
        (
            rect.centerx - image.get_width() // 2,
            rect.centery - image.get_height() // 2,
        ),
    )


def draw_hud(
    screen, health, score, level, max_level, time_left,
    kills, level_target, fonts
):
    font, small_font, medium_font = fonts

    pygame.draw.rect(
        screen,
        DARK,
        (0, PLAY_HEIGHT, WIDTH, HEIGHT - PLAY_HEIGHT),
    )

    pygame.draw.line(
        screen,
        GREEN,
        (0, PLAY_HEIGHT),
        (WIDTH, PLAY_HEIGHT),
        3,
    )

    draw_text(
        screen, "HEALTH", small_font, WHITE,
        15, PLAY_HEIGHT + 10
    )

    pygame.draw.rect(
        screen,
        (75, 75, 75),
        (90, PLAY_HEIGHT + 12, 150, 18),
        border_radius=5,
    )

    health_width = int(150 * health / 100)

    if health_width > 0:
        health_color = GREEN if health > 30 else RED

        pygame.draw.rect(
            screen,
            health_color,
            (90, PLAY_HEIGHT + 12, health_width, 18),
            border_radius=5,
        )

    draw_text(
        screen, f"{health}/100", small_font, WHITE,
        250, PLAY_HEIGHT + 12
    )

    draw_text(
        screen, f"SCORE: {score}", font, YELLOW,
        350, PLAY_HEIGHT + 8
    )

    draw_text(
        screen, f"LEVEL: {level}/{max_level}", font, WHITE,
        550, PLAY_HEIGHT + 8
    )

    timer_color = RED if time_left <= 15 else WHITE

    import math

    draw_text(
        screen,
        f"TIME: {max(0, math.ceil(time_left))}s",
        font,
        timer_color,
        730,
        PLAY_HEIGHT + 8,
    )

    draw_text(
        screen, f"ZOMBIES: {kills}/{level_target}",
        small_font, GREEN, 15, PLAY_HEIGHT + 48
    )

    draw_text(
        screen, "WASD/ARROWS: MOVE",
        small_font, WHITE, 220, PLAY_HEIGHT + 48
    )

    draw_text(
        screen, "LEFT CLICK: SHOOT",
        small_font, WHITE, 430, PLAY_HEIGHT + 48
    )

    pause_button = pygame.Rect(
        720, PLAY_HEIGHT + 42, 160, 38
    )

    draw_button(
        screen, "PAUSE (P)", pause_button,
        (75, 85, 95), medium_font
    )

    return pause_button