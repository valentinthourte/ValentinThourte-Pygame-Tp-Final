
from gui.gui_factory import GuiFactory
from level_helper import LevelHelper
from constantes import *


class GuiHelper:
    @staticmethod
    def initialize_gui_forms(screen):
        GuiFactory.create_start_form(screen, w=ANCHO_VENTANA, h=ALTO_VENTANA, active=True)
        GuiFactory.create_settings_form(screen, w=MENU_FORM_WIDTH, h=MENU_FORM_HEIGHT, active=False)
        GuiFactory.create_rankings_form(screen, w=MENU_FORM_WIDTH, h=MENU_FORM_HEIGHT, active=False)
        LevelHelper.create_all_levels(screen)


        

    