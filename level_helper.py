from constantes import *
from gui.gui_form import Form
from levels.L2.gui_form_menu_game_l2_MP import FormGameLevel2_MP

from levels.L2.gui_form_menu_game_l2_SP import FormGameLevel2_SP
from levels.l1.gui_form_menu_game_l1_MP import FormGameLevel1_MP
from levels.l1.gui_form_menu_game_l1_SP import FormGameLevel1_SP


class LevelHelper():
    

    @staticmethod
    def get_level_2_sp(screen):
        return FormGameLevel2_SP(name="L2_SP",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)
    
    @staticmethod
    def get_level_1_sp(screen):
        return FormGameLevel1_SP(name="L1_SP",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)
    @staticmethod
    def get_level_2_mp(screen):
        return FormGameLevel2_MP(name="L2_MP",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)
        
    @staticmethod
    def get_level_1_mp(screen):
        return FormGameLevel1_MP(name="L1_MP",master_surface = screen,x=0,y=0,w=ANCHO_VENTANA,h=ALTO_VENTANA,color_background=(0,255,255),color_border=(255,0,255),active=False)
    
    @staticmethod
    def get_level_by_name(name):
        
        Form.forms_dict.pop(name)
        match name:
            case "L1_SP":
               return LevelHelper.get_level_1_sp()
            case "L2_SP":
               return LevelHelper.get_level_2_sp()
            case "L1_MP":
               return LevelHelper.get_level_1_mp()
            case "L2_MP":
               return LevelHelper.get_level_2_mp()