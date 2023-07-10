import pygame
from pygame.locals import *
from background import Background
from constantes import *
from gui.gui_form import Form
from gui.gui_button import Button
from gui.gui_textbox import TextBox
from gui.gui_progressbar import ProgressBar
from gui.widget_factory import WidgetFactory


class StartMenuForm(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)
        self.create_background()
        self.create_text()
        self.boton_singleplayer = Button(master=self,x=20,y=140,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.on_click_next_form,on_click_param="form_game_L1_SP",text="JUGAR SINGLEPLAYER",font="Verdana",font_size=12,font_color=C_WHITE)
        self.boton_multiplayer = Button(master=self,x=20,y=200,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.on_click_next_form,on_click_param="form_game_L1_MP",text="JUGAR MULTIPLAYER",font="Verdana",font_size=12,font_color=C_WHITE)
        self.boton_settings = WidgetFactory.get_settings_button(self, 20, 260, self.on_click_next_form)

        self.widget_list += [self.boton_singleplayer, self.boton_multiplayer, self.boton_settings]

    def create_background(self):
        img = pygame.image.load(START_IMAGE_PATH)
        x,y = self.slave_rect.center
        image_x = x - img.get_width() // 2
        image_y = ALTO_VENTANA - img.get_height()
        self.background = Background(image_x,image_y,ANCHO_VENTANA,ALTO_VENTANA,START_IMAGE_PATH, False)
    
    def create_text(self):
        # font = pygame.font.Font("images/assets/fonts/BreatheFireIv-3zAVZ.ttf", 100)
        font = pygame.font.Font("images/assets/fonts/ConflictDripsPersonalUseBold-WyKXn.ttf", 100)
        
        text = GAME_TITLE
        self.text = font.render(text, True, C_RED)     
        text_width = self.text.get_width()

        # Calculate the position to center the text above the image
        self.text_x = self.slave_rect.centerx - text_width // 2
        self.text_y = 100

    def on_click_next_form(self, parametro):
        self.set_active(parametro)

    def update(self, lista_eventos,keys,delta_ms):
        super().update(lista_eventos)
    
    def draw(self):
        super().draw()
        self.background.draw(self.master_surface)
        self.master_surface.blit(self.text, (self.text_x, self.text_y))