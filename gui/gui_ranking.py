

from background import Background
from db_helper import DBHelper
from gui.gui_form import Form
from constantes import *
from gui.gui_button import Button

class RankingForm(Form):
    def __init__(self, name, master_surface, x, y, w, h, color_background, color_border, active):
        super().__init__(name, master_surface, x, y, w, h, color_background, color_border, active)
        self.scores = DBHelper.get_scores()[:5]
        button_w = 45
        button_h = 45
        self.button_back = Button(master=self,x=30,y=30,w=button_w,h=button_h,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=Form.return_to_last_from,on_click_param="",text="<--",font="Verdana",font_size=16,font_color=C_WHITE)

        self.widget_list = [self.button_back]
    

    def draw(self):
        self.master_surface.fill(C_BLACK)
        super().draw()
        font = pygame.font.Font(BLOOD_FONT_PATH, 100)
        
        text = "Rankings"
        title = font.render(text, True, C_BLOOD)     
        text_width = title.get_width()
        title_x = self.slave_rect.centerx - text_width // 2
        title_y = 100
        self.master_surface.blit(title, (title_x, title_y))
        score_y = 200
        score_x = title_x
        font = pygame.font.Font("images/assets/fonts/SomethingStrange-vjYD.ttf", 60)
        for score in self.scores:
            score_text = f"{score[1]}: {score[2]}"
            score_y += 50
            score = font.render(score_text, (score_x, score_y), C_RED)
            self.master_surface.blit(score, (score_x, score_y))

        for widget in self.widget_list:
            widget.draw()
    
    def update(self, lista_eventos,keys,delta_ms):
        return super().update(lista_eventos)
