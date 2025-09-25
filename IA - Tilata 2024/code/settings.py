import pygame
from os import walk

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 608
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 30
TILESIZE = 16
VOID_COLOR = (0,15,13)

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 240
ENERGY_BAR_WIDTH = 140
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
HEALTH_COLOR = (160,24,13)
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
UI_SELECTED_COLOR = 'gold'
TEXT_COLOR = '#EEEEEE'
WHITE = (255,255,255)
BLACK = (0,0,0)

# MUSIC
menu_song = pygame.mixer.Sound("SFX/Cherry Cola.mp3")
pygame.mixer.music.load("SFX/Coffee at Night.mp3")
# FONTS
main_font = pygame.font.Font('graphics/font/OpenSans-Regular.ttf', 18)
font1 = pygame.font.Font('graphics/font/OpenSans-Regular.ttf', 28)
font_UI = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

base_map = pygame.image.load(f'map/maps_ia.png')

def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        img_files = sorted(img_files)
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


def draw_text(text, font, text_col, x, y):
     img = font.render(text, True, text_col)
     screen.blit(img, (x,y))

information = [
    ' "La llegada de la IA marca un nuevo capítulo en la evolución tecnológica\ny laboral. A pesar de los retos significativos, la historia demuestra la\ncapacidad de la humanidad para adaptarse en un mundo tecnológico. La clave\nestá en abordar, desde hoy, los desafíos de manera ética y responsable,\nasegurando que la IA beneficie a toda la sociedad mediante una regulación adecuada."\nWIRED',
    ]