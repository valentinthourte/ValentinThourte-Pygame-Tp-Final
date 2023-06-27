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
from abc import ABC, abstractmethod
from enemy_factory import EnemyFactory
from platform_factory import PlatformFactory


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

        self.enemy_list = [EnemyFactory.get_ogre_enemy(450,400,self), EnemyFactory.get_ogre_enemy(900, 400, self)]

        self.platform_list = PlatformFactory.get_platforms_for_level(LEVEL_1)

        self.has_won = False

        self.player_list = []

        self.create_player()

    @abstractmethod
    def create_player(self):
        pass
    
    @abstractmethod
    def create_victory(self):
        pass

    def update(self, lista_eventos,keys,delta_ms, player_list):
        self.check_victory()
        if not self.freeze():
            for aux_widget in self.widget_list:
                aux_widget.update(lista_eventos)
                
            for bullet_element in self.bullet_list:
                bullet_element.update(delta_ms,self.platform_list,self.enemy_list,player_list)

            for enemy_element in self.enemy_list:
                enemy_element.update(delta_ms,self.platform_list, player_list)
        
        self.pb_lives.value = self.player_1.lives 

    
    def draw(self): 
            super().draw()
            self.static_background.draw(self.surface)

            for aux_widget in self.widget_list:    
                aux_widget.draw()

            for plataforma in self.platform_list:
                plataforma.draw(self.surface)

            for enemy_element in self.enemy_list:
                enemy_element.draw(self.surface)
    
    def player_shoot(self, bullet):
        self.bullet_list.append(bullet)
    
    def get_colliding_enemies(self, player):
        colliding_enemy_list = []
        for enemy in self.enemy_list:
            if CollisionHelper.player_colliding_with_entity(player, enemy):
                colliding_enemy_list.append(enemy)
        return colliding_enemy_list
    
    
    def kill_enemy(self, enemy: Enemy):
        self.enemy_list.remove(enemy)

    def check_victory(self):
        if CollisionHelper.player_colliding_with_entity(self.player_1, self.victory):
            self.has_won = True
            if self.victory.show_victory(self.surface):
                # Form.set_active(NAME_FORM_MENU_B)
                pass
    
    def player_can_update(self, player):
        return not player.is_dead and not self.freeze()
    
    def freeze(self):
        return self.has_won