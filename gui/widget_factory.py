from constantes import *
from gui.gui_button import Button
from gui.gui_form import Form
from levels.level import Level


class WidgetFactory:
    @staticmethod
    def get_settings_button(master, x, y, on_click):
        return Button(master=master,x=x,y=y,w=200,h=50,color_background=C_BLOOD,color_border=C_BLACK, image_background=None, text="Settings", font=BLOOD_FONT_PATH, font_size=14, font_color=C_WHITE, on_click=on_click,on_click_param=SETTINGS_MENU_NAME)

    @staticmethod
    def get_back_button(master, x, y, on_click):
        return Button()

    @staticmethod
    def get_next_level_button(master,x,y,parameter):
        return Button(master,x,y, w=400, h=200,color_background=C_BLOOD,color_border=C_BLACK, text="Next Level", font=BLOOD_FONT_PATH,font_size=40,on_click=Form.set_active, on_click_param=parameter)
    
    @staticmethod
    def get_final_button(master,x,y,parameter):
        return Button(master,x,y, w=400, h=200,color_background=C_RED,color_border=C_BLACK, text="Quit", font=BLOOD_FONT_PATH,font_size=40,on_click=Level.quit, on_click_param=parameter)
    
    @staticmethod
    def get_restart_button(master,x,y,function,parameter):
        return Button(master,x,y, w=400, h=200,color_background=C_RED,color_border=C_BLACK, text="Restart level", font=BLOOD_FONT_PATH,font_size=40,on_click=function, on_click_param=parameter)
        