import pygame
from . import constants as C
from . import tools
from source.state import menu, level,level3
import random

pygame.init()
SCREEN = pygame.display.set_mode(C.SCREEN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Flappy Bird')
img = pygame.image.load("flappy_bird.ico")
pygame.display.set_icon(img)

GRAPHICS = tools.load_graphics("resources//graphics")

CHONG = tools.load_graphics("resources//chong")

FONT_big = tools.get_font()['big']
FONT_small = tools.get_font()['small']

random = random.random() * 2

rank_list = tools.get_rank("./resources/rank.txt")
rank_list1 = tools.get_rank("./resources/rank1.txt")


STATE_DICT = {
    'menu': menu.Menu(),
    'level': level.Level(),
    'rank': level3.Level()
}
