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
from player_factory import PlayerFactory

class FormGameLevel1_SP(FormGameLevel1):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)

        self.create_player()
        self.create_victory()


    def create_player(self):
        self.player_1 = PlayerFactory.get_player(1, 0, 400, self, PATH_COWGIRL_IMAGES, PLAYER_1_KEYS)
        self.player_list = self.player_1

    def create_victory(self):
        self.victory = Victory(SINGLEPLAYER_VICTORY_IMAGE_PATH, 88, 463, 1400, 137, 200)

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
            self.player_1.update(delta_ms,self.platform_list)


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