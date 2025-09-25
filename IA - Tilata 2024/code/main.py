import pygame
import spritesheet
from level import Level
from questions import *
from settings import *
from menus import *

pygame.init()
pygame.display.set_caption('The Code Game')
# TILEMAP
sprite_sheet_image = pygame.image.load('map/final_tile.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
level = Level('map/map1_ main.csv', 'map/map1_decoration.csv', 'map/map1_entities.csv', sprite_sheet)

pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)                     
pygame.mixer.music.pause()
menu_song.play()
menu_song.set_volume(0.1)
Intro = True
while Intro:
    clock.tick(FPS)
    key = pygame.key.get_pressed()
    screen.fill(VOID_COLOR)
    draw_text("Concurso The Code Game 2024", font1, (235, 210, 127), (SCREEN_WIDTH/2)-100,(SCREEN_HEIGHT/2)-150)
    draw_text("Teras: Explorando el Alcance e Impacto de la Inteligencia Artificial", main_font, (255, 255, 255), (SCREEN_WIDTH/2)-250,(SCREEN_HEIGHT/2)-100)
    draw_text("Presiona 'M' para empezar el juego", font_UI, (175, 77 ,73), (SCREEN_WIDTH/2)-250,(SCREEN_HEIGHT/2)+50)
    draw_text("Presiona 'T' para ver guía", font_UI, (175, 77 ,73), (SCREEN_WIDTH/2)-200,(SCREEN_HEIGHT/2))
        
    if key[pygame.K_m]:     
        Intro = False
        pygame.mixer.fadeout(1000)
    if key[pygame.K_t]:
        guide()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            Intro = False
            quit()
    pygame.display.update()

pygame.mixer.music.unpause()
run = True
while run:
    dt = clock.tick(FPS) * 0.001 * FPS
    screen.fill(VOID_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    key = pygame.key.get_pressed()        
    if key[pygame.K_ESCAPE]:
        pygame.mouse.set_visible(True)
        pause()

    level.load_map()
    pygame.display.update()
pygame.quit()