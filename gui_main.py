import pygame
from pygame.locals import *
import sys
from constantes import *
from gui_form import Form
from gui_form_menu_A import FormMenuA
from gui_form_menu_B import FormMenuB
from gui_form_menu_C import FormMenuC
from levels.l1.gui_form_menu_game_l1_MP import FormGameLevel1_MP
from levels.l1.gui_form_menu_game_l1_SP import FormGameLevel1_SP


flags = DOUBLEBUF 
screen = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA), flags, 16)
pygame.init()
clock = pygame.time.Clock()

form_menu_A = FormMenuA(name="form_menu_A",master_surface = screen,x=300,y=200,w=500,h=400,color_background=(255,255,0),color_border=(255,0,255),active=True)
form_menu_B = FormMenuB(name=NAME_FORM_MENU_B,master_surface = screen,x=300,y=200,w=500,h=400,color_background=(0,255,255),color_border=(255,0,255),active=False)
form_menu_C = FormMenuC(name="form_menu_C",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)

form_game_L1_sp = FormGameLevel1_SP(name="form_game_L1_SP",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)
form_game_L1_mp = FormGameLevel1_MP(name="form_game_L1_MP",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)

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

