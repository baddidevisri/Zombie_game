import pygame

# Window settings
WIDTH = 900
HEIGHT = 700
HUD_HEIGHT = 90
PLAY_HEIGHT = HEIGHT - HUD_HEIGHT
TILE = 40

# Colors
BLACK = (10, 15, 18)
DARK = (20, 30, 32)
DARK_GREEN = (18, 80, 39)
GREEN1 = (35, 145, 60)
GREEN2 = (42, 160, 65)
WALL = (30, 48, 38)
WALL_LIGHT = (75, 100, 75)
WHITE = (245, 245, 235)
RED = (235, 55, 55)
YELLOW = (255, 210, 45)
BLUE = (45, 145, 245)
GREEN = (60, 220, 100)
ORANGE = (255, 145, 45)

# Game settings
PLAYER_SPEED = 3.5
BULLET_SPEED = 9
LEVEL_TIME = 90
MAX_LEVEL = 5

# Game states
MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
LEVEL_COMPLETE = "level_complete"
GAME_OVER = "game_over"
VICTORY = "victory"