
from gui.gui_form_menu_A import FormMenuA
from gui.gui_form_menu_B import FormMenuB
from gui.gui_form_menu_C import FormMenuC
from gui.gui_factory import GuiFactory
from gui.gui_settings_form import SettingsForm
from levels.l1.gui_form_menu_game_l1_MP import FormGameLevel1_MP
from levels.l1.gui_form_menu_game_l1_SP import FormGameLevel1_SP
from constantes import *


class GuiHelper:
    @staticmethod
    def initialize_gui_forms(screen):
        GuiFactory.create_start_form(screen, w=MENU_FORM_WIDTH, h=MENU_FORM_HEIGHT, active=True)
        GuiFactory.create_settings_form(screen, w=MENU_FORM_WIDTH, h=MENU_FORM_HEIGHT, active=False)

        FormMenuB(name=NAME_FORM_MENU_B,master_surface = screen,x=300,y=200,w=500,h=400,color_background=(0,255,255),color_border=(255,0,255),active=False)
        FormMenuC(name="form_menu_C",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)
        FormGameLevel1_SP(name="form_game_L1_SP",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)
        FormGameLevel1_MP(name="form_game_L1_MP",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)
        
class GuiFactory:
    @staticmethod
    def create_start_form(master_surface, w, h, active):
        x,y = GuiFactory.get_coordinates_for_surface_from_sizes(master_surface, w, h)
        FormMenuA(name=START_MENU_NAME,master_surface = master_surface,x=x,y=y,w=w,h=h,color_background=(255,255,0),color_border=(255,0,255),active=active)
        
    @staticmethod
    def create_settings_form(master_surface, w, h, active):
        x,y = GuiFactory.get_coordinates_for_surface_from_sizes(master_surface, w, h)
        SettingsForm(name=SETTINGS_MENU_NAME, master_surface=master_surface, x=x,y=y,w=w,h=h,color_background=(0,0,0),color_border=(0,0,0), active=active)
        
        
    @staticmethod
    def get_coordinates_for_surface_from_sizes(master_surface, w, h):
        return GuiFactory.get_coordinates_from_sizes(master_surface.get_width(), master_surface.get_height(), w, h)
    
    @staticmethod
    def get_coordinates_from_sizes(surface_width, surface_height, element_width, element_height):
        x = (surface_width - element_width) / 2
        y = (surface_height / 2) - (element_height / 2)
        return x,y
    