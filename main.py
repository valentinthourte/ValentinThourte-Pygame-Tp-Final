import pygame
from pygame.locals import *
import sys
from constantes import *
from db_helper import DBHelper
from gui.gui_form import Form
from gui.gui_form_menu_A import FormMenuA
from gui.gui_form_menu_B import FormMenuB
from gui.gui_form_menu_C import FormMenuC
from gui.gui_helper import GuiHelper
from levels.l1.gui_form_menu_game_l1_MP import FormGameLevel1_MP
from levels.l1.gui_form_menu_game_l1_SP import FormGameLevel1_SP

flags = DOUBLEBUF 
screen = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA), flags, 16)
pygame.display.set_caption(GAME_TITLE)
pygame.init()
clock = pygame.time.Clock()

GuiHelper.initialize_gui_forms(screen)

while True:     
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    print(pygame.mouse.get_pos())
    #CAPAZ POR ANIMACIONES BUG AL CORRER
    keys = pygame.key.get_pressed()
    delta_ms = clock.tick(FPS)

    aux_form_active = Form.get_active()
    if(aux_form_active != None):
        aux_form_active.update(lista_eventos,keys,delta_ms)
        aux_form_active.draw()

    pygame.display.flip()

