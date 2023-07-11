import pygame
import pygame.mixer

from pygame.locals import *
import sys
from constantes import *
from gui.gui_form import Form
from gui.gui_helper import GuiHelper

flags = DOUBLEBUF 
screen = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA), flags, 16)
pygame.display.set_caption(GAME_TITLE)
pygame.init()
clock = pygame.time.Clock()

GuiHelper.initialize_gui_forms(screen)
pygame.mixer.init()
pygame.mixer.music.load(MUSIC_PATH)
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)

while True:     
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    delta_ms = clock.tick(FPS)

    aux_form_active = Form.get_active()
    if(aux_form_active != None):
        aux_form_active.update(lista_eventos,keys,delta_ms)
        aux_form_active.draw()

    pygame.display.flip()

