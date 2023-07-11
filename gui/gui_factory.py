from constantes import *
from gui.gui_form import Form
from gui.gui_settings_form import SettingsForm
from gui.gui_start_menu import StartMenuForm
from gui.gui_you_win import FormYouWin


class GuiFactory:
    @staticmethod
    def create_start_form(master_surface, w, h, active):
        x,y = GuiFactory.get_coordinates_for_surface_from_sizes(master_surface, w, h)
        StartMenuForm(name=START_MENU_NAME,master_surface = master_surface,x=x,y=y,w=w,h=h,color_background=(0,0,0),color_border=(255,0,0),active=active)
        
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
    
    @staticmethod
    def create_you_win_form(screen, next_level):
        Form.remove(YOU_WIN_FORM_NAME)
        FormYouWin(YOU_WIN_FORM_NAME, screen, 0,0,ANCHO_VENTANA,ALTO_VENTANA,C_BLACK,None,False, next_level)