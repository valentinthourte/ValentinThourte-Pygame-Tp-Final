import pygame
from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
from gui_progressbar import ProgressBar
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from bullet import Bullet
from collision_helper import CollisionHelper
from victory import Victory

class FormGameLevel1(Form):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)

        # --- GUI WIDGET --- 
        self.boton1 = Button(master=self,x=0,y=0,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.on_click_boton1,on_click_param="form_menu_B",text="BACK",font="Verdana",font_size=30,font_color=C_WHITE)
        self.boton2 = Button(master=self,x=200,y=0,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.on_click_boton1,on_click_param="form_menu_B",text="PAUSE",font="Verdana",font_size=30,font_color=C_WHITE)
        self.boton_shoot = Button(master=self,x=400,y=0,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.on_click_shoot,on_click_param="form_menu_B",text="SHOOT",font="Verdana",font_size=30,font_color=C_WHITE)
       
        self.pb_lives = ProgressBar(master=self,x=500,y=50,w=240,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Bars/Bar_Background01.png",image_progress="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",value = 5, value_max=5)
        self.widget_list = [self.boton1,self.boton2,self.pb_lives,self.boton_shoot]

        # --- GAME ELEMNTS --- 
        self.static_background = Background(x=0,y=0,width=w,height=h,path="images/locations/set_bg_01/forest/all.png")

        self.bullet_list = []

        # self.player_1 = Player(x=0,y=400,speed_walk=10,speed_run=15,gravity=14,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140, owner=self,p_scale=0.2,interval_time_jump=300)
        self.player_1 = Player(x=0,y=400,speed_walk=50,speed_run=80,gravity=14,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140, owner=self,p_scale=0.2,interval_time_jump=300)

        self.enemy_list = []
        self.enemy_list.append (Enemy(x=450,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140, owner=self,p_scale=0.08,interval_time_jump=300))
        self.enemy_list.append (Enemy(x=900,y=400,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140, owner=self,p_scale=0.08,interval_time_jump=300))

        self.plataform_list = []
        self.plataform_list.append(Plataform(x=400,y=500,width=50,height=50,type=0))
        self.plataform_list.append(Plataform(x=450,y=500,width=50,height=50,type=1))
        self.plataform_list.append(Plataform(x=500,y=500,width=50,height=50,type=2))   
        self.plataform_list.append(Plataform(x=600,y=430,width=50,height=50,type=12))
        self.plataform_list.append(Plataform(x=650,y=430,width=50,height=50,type=14))
        self.plataform_list.append(Plataform(x=750,y=360,width=50,height=50,type=12))
        self.plataform_list.append(Plataform(x=800,y=360,width=50,height=50,type=13))
        self.plataform_list.append(Plataform(x=850,y=360,width=50,height=50,type=13))
        self.plataform_list.append(Plataform(x=900,y=360,width=50,height=50,type=14))

        self.victory = Victory(VICTORY_IMAGE_PATH, 88, 463, 1400, 137, 200)

        self.has_won = False


    def on_click_boton1(self, parametro):
        self.set_active(parametro)

    def on_click_shoot(self, parametro):
        for enemy_element in self.enemy_list:
            self.bullet_list.append(Bullet(enemy_element,enemy_element.rect.centerx,enemy_element.rect.centery,self.player_1.rect.centerx,self.player_1.rect.centery,20,path="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",frame_rate_ms=100,move_rate_ms=20,width=5,height=5))

        

    def update(self, lista_eventos,keys,delta_ms):

        self.check_victory()
        if not self.freeze():
            for aux_widget in self.widget_list:
                aux_widget.update(lista_eventos)

            for bullet_element in self.bullet_list:
                bullet_element.update(delta_ms,self.plataform_list,self.enemy_list,self.player_1)

            for enemy_element in self.enemy_list:
                enemy_element.update(delta_ms,self.plataform_list, self.player_1)


        if self.player_can_update():
            self.player_1.events(delta_ms,keys)
            self.player_1.update(delta_ms,self.plataform_list)


        self.pb_lives.value = self.player_1.lives 


    def draw(self): 
        super().draw()
        self.static_background.draw(self.surface)

        for aux_widget in self.widget_list:    
            aux_widget.draw()

        for plataforma in self.plataform_list:
            plataforma.draw(self.surface)

        for enemy_element in self.enemy_list:
            enemy_element.draw(self.surface)
        
        self.player_1.draw(self.surface)

        for bullet_element in self.bullet_list:
            bullet_element.draw(self.surface)
        
        self.victory.draw(screen=self.surface)

    def player_shoot(self, bullet):
        self.bullet_list.append(bullet)
    
    def get_colliding_enemies(self, player):
        colliding_enemy_list = []
        for enemy in self.enemy_list:
            if CollisionHelper.player_colliding_with_entity(player, enemy):
                colliding_enemy_list.append(enemy)
        return colliding_enemy_list
    
    
    def kill(self, enemy: Enemy):
        self.enemy_list.remove(enemy)

    def check_victory(self):
        if CollisionHelper.player_colliding_with_entity(self.player_1, self.victory):
            self.has_won = True
            if self.victory.show_victory(self.surface):
                # Form.set_active(NAME_FORM_MENU_B)
                pass
    
    def player_can_update(self):
        return not self.player_1.is_dead and not self.freeze()
    
    def freeze(self):
        return self.has_won