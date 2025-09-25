
import pygame
from settings import *

def pause():
    pause = True
    if pause == True:
        menu_song.play()
        menu_song.set_volume(0.1)
        pygame.mixer.music.pause()
    while pause:      
        clock.tick(30)
        key = pygame.key.get_pressed()
        screen.fill(VOID_COLOR)
        draw_text("GAME PAUSED", font1, (254, 249 ,129), (SCREEN_WIDTH/2)-100,( SCREEN_HEIGHT/2)-200)
        draw_text("Presiona 'm' para continuar", font_UI, (175, 77 ,73), (SCREEN_WIDTH/2)-190,( SCREEN_HEIGHT/2)-80)
        draw_text("Presiona 't' para ver guía", font_UI, (175, 77 ,73), (SCREEN_WIDTH/2)-170,( SCREEN_HEIGHT/2)+35)
        draw_text("Presiona 'q' para salir del juego", font_UI, (175, 77 ,73), (SCREEN_WIDTH/2)-200,( SCREEN_HEIGHT/2)+150)

        if key[pygame.K_t]:
            guide()
        if key[pygame.K_m]:
            pause = False
            pygame.mixer.fadeout(1000)
            pygame.mixer.music.unpause()

        if key[pygame.K_q]:
            quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                quit()
        pygame.display.update()

def guide():
    guide = True
    while guide:      
        clock.tick(30)
        key = pygame.key.get_pressed()
        screen.fill(VOID_COLOR)
        draw_text("GUÍA", font_UI, (254, 249 ,129), (SCREEN_WIDTH/2)-315,( SCREEN_HEIGHT/2)-280)
        draw_text("Contexto: has sido encarcelado por ser un", font1, WHITE,60,( SCREEN_HEIGHT/2)-250)
        draw_text("desconocedor del impacto y relevancia de las IAs.", font1, WHITE, 60,( SCREEN_HEIGHT/2)-210)
        draw_text("Propósito: Encuentra todas las llaves esparcidas ", font1, WHITE, 60,( SCREEN_HEIGHT/2)-160)
        draw_text("por el mapa para desbloquear la salida de la prisión", font1,WHITE , 60,( SCREEN_HEIGHT/2)-120)
        draw_text("y ser libre. Responde preguntas sobre la IA en el camino.", font1, WHITE, 60,( SCREEN_HEIGHT/2)-80)
        draw_text("Controles:", font_UI, (254, 249 ,129), 80,( SCREEN_HEIGHT/2))
        draw_text("Presiona SPACE BAR para atacar a los enemigos", font1, WHITE, 60,( SCREEN_HEIGHT/2)+40)
        draw_text("y usa las flechas para mover al jugador.", font1,WHITE , 60,( SCREEN_HEIGHT/2)+80)
        draw_text("Puedes pausar el juego usando la tecla ESCAPE.", font1,WHITE , 60,( SCREEN_HEIGHT/2)+120)
        draw_text("presiona '1' para volver.", font_UI, (212,154,53), 400, SCREEN_HEIGHT-40)
        if key[pygame.K_1]:
            guide = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                quit()
        pygame.display.update()