
from constantes import *
from gui.gui_button import Button


class WidgetFactory:
    @staticmethod
    def get_settings_button(master, x, y, on_click):
        return Button(master=master,x=x,y=y,w=200,h=50,color_background=C_GREEN,color_border=C_BLACK, image_background=None, text="Settings", font="Arial", font_size=14, font_color=C_WHITE, on_click=on_click,on_click_param=SETTINGS_MENU_NAME)

    @staticmethod
    def get_back_button(master, x, y, on_click):
        return Button()