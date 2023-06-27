import pygame
from pygame.locals import *
from constantes import *
from gui_form import Form
from gui_button import Button
from gui_textbox import TextBox
from gui_progressbar import ProgressBar
from levels.l1.gui_form_menu_game_l1 import FormGameLevel1
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from bullet import Bullet
from collision_helper import CollisionHelper
from victory import Victory

class FormGameLevel1_MP(FormGameLevel1):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)
        self.create_player()
        self.create_victory()


    def create_player(self):
        id_player_1 = 1
        id_player_2 = 2
        
        self.player_1 = Player(1,x=30,y=400,speed_walk=50,speed_run=80,gravity=14,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140, owner=self, images_path=PATH_COWGIRL_IMAGES, player_keys=PLAYER_1_KEYS, p_scale=0.2,interval_time_jump=300)
        self.player_2 = Player(2,x=30,y=400,speed_walk=50,speed_run=80,gravity=14,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140, owner=self, images_path=PATH_COWBOY_IMAGES, player_keys=PLAYER_2_KEYS, p_scale=0.2,interval_time_jump=300)
        
        self.player_key_list = {id_player_1: PLAYER_1_KEYS, id_player_2: PLAYER_2_KEYS}
        self.player_list = [self.player_1, self.player_2]
    
    def create_victory(self):
        self.victory = Victory(MULTIPLAYER_VICTORY_IMAGE_PATH, 88, 463, 1400, 137, 200)

    def on_click_boton1(self, parametro):
        self.set_active(parametro)

    def on_click_shoot(self, parametro):
        for enemy_element in self.enemy_list:
            self.bullet_list.append(Bullet(enemy_element,enemy_element.rect.centerx,enemy_element.rect.centery,self.player_1.rect.centerx,self.player_1.rect.centery,20,path="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",frame_rate_ms=100,move_rate_ms=20,width=5,height=5))


    def update(self, lista_eventos,keys,delta_ms, player_list = None):
        if not player_list:
            player_list = self.player_list

        super().update(lista_eventos,keys,delta_ms, player_list)

        for player in self.player_list:
            if self.player_can_update(player):
                player.events(delta_ms,keys)
            player.update(delta_ms,self.platform_list)


        self.pb_lives.value = self.player_1.lives 


    def draw(self): 
        super().draw()
    
        for player in self.player_list:
            player.draw(self.surface)
        
        self.victory.draw(screen=self.surface)

    