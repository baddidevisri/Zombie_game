import pygame
from settings import WIDTH, PLAY_HEIGHT

walls = [
    pygame.Rect(160, 80, 80, 40),
    pygame.Rect(280, 160, 40, 120),
    pygame.Rect(440, 80, 40, 120),
    pygame.Rect(520, 240, 120, 40),
    pygame.Rect(120, 320, 120, 40),
    pygame.Rect(320, 360, 80, 40),
    pygame.Rect(440, 440, 120, 40),
    pygame.Rect(640, 360, 40, 80),
    pygame.Rect(200, 440, 40, 80),
    pygame.Rect(360, 120, 40, 40),
    pygame.Rect(560, 400, 40, 40),
    pygame.Rect(720, 120, 40, 120),
    pygame.Rect(720, 500, 80, 40),
]


def blocked(position, radius=14):
    box = pygame.Rect(
        int(position.x - radius),
        int(position.y - radius),
        radius * 2,
        radius * 2,
    )

    if position.x < radius or position.x > WIDTH - radius:
        return True

    if position.y < radius or position.y > PLAY_HEIGHT - radius:
        return True

    return any(box.colliderect(wall) for wall in walls)


def move_safely(position, movement, radius=14):
    # Horizontal movement
    test = pygame.Vector2(
        position.x + movement.x,
        position.y
    )

    if not blocked(test, radius):
        position.x = test.x

    # Vertical movement
    test = pygame.Vector2(
        position.x,
        position.y + movement.y
    )

    if not blocked(test, radius):
        position.y = test.y


def draw_walls(screen, wall_color, wall_light):
    for wall in walls:
        pygame.draw.rect(
            screen, wall_color, wall, border_radius=5
        )

        pygame.draw.rect(
            screen,
            wall_light,
            (
                wall.x + 4,
                wall.y + 4,
                wall.width - 8,
                wall.height - 8,
            ),
            border_radius=4,
        )