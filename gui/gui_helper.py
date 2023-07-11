
from gui.gui_factory import GuiFactory
from level_helper import LevelHelper
from constantes import *


class GuiHelper:
    @staticmethod
    def initialize_gui_forms(screen):
        GuiFactory.create_start_form(screen, w=ANCHO_VENTANA, h=ALTO_VENTANA, active=True)
        GuiFactory.create_settings_form(screen, w=MENU_FORM_WIDTH, h=MENU_FORM_HEIGHT, active=False)
        
        LevelHelper.get_level_1_sp(screen)  
        LevelHelper.get_level_2_sp(screen)  
        LevelHelper.get_level_1_mp(screen)  
        LevelHelper.get_level_2_mp(screen) 
        

    