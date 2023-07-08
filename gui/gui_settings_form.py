from background import Background
from gui.gui_form import Form
from constantes import *
from gui.gui_label import Label
import gui.gui_helper  

class SettingsForm(Form):
    def __init__(self, name, master_surface, x, y, w, h, color_background, color_border, active):
        super().__init__(name, master_surface, x, y, w, h, color_background, color_border, active)
        self.create_background_images(w, h)
        self.create_widgets(w,h)
    
    def update(self, lista_eventos,keys,delta_ms):
        super().update(lista_eventos)
    
    def draw(self):
        for image in self.image_list:
            image.draw(self.master_surface)
        
        super().draw()

    def create_widgets(self, w,h):
        master_rect = self.master_surface.get_rect()
        labels_x = master_rect.left + (w / 4)
        y = master_rect.top + 60
        self.widget_list.append(Label(master=self,x=labels_x,y=y,w=140,h=50,color_background=None,color_border=None,image_background=None,text="Music",font="Verdana",font_size=12,font_color=C_BLACK))

    def create_background_images(self, w, h):
        x,y = gui.gui_helper.GuiFactory.get_coordinates_for_surface_from_sizes(self.master_surface, w, h)
        self.image_list = []
        self.image_list.append(Background(x=x,y=y,width=w,height=h,path="images/gui/jungle/settings/bg.png"))
        delta_table_size = 40
        delta_table_pos = delta_table_size / 2
        self.image_list.append(Background(x=x + delta_table_pos,y=y + delta_table_pos,width=w - delta_table_size,height=h - delta_table_size,path="images/gui/jungle/settings/table.png"))
        delta_settings_pos = delta_table_pos + 150
        self.image_list.append(Background(x=x + delta_settings_pos, y=self.master_surface.get_rect().top, width=500, height=200, path="images/gui/jungle/settings/92.png"))

