import pygame
from pygame.locals import *
import constantes
import random
# from constantes import *
from gui.gui_form import Form
from gui.gui_button import Button
from gui.gui_textbox import TextBox
from gui.gui_progressbar import ProgressBar
from health_consumable import HealthConsumable
from levels.level import Level
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


class FormGameLevel1(Level):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)

        # --- GUI WIDGET --- 
        self.boton1 = Button(master=self,x=0,y=0,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.on_click_boton1,on_click_param="form_menu_B",text="BACK",font="Verdana",font_size=30,font_color=constantes.C_WHITE)
        self.boton2 = Button(master=self,x=200,y=0,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.on_click_boton1,on_click_param="form_menu_B",text="PAUSE",font="Verdana",font_size=30,font_color=constantes.C_WHITE)
        self.boton_shoot = Button(master=self,x=400,y=0,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.on_click_shoot,on_click_param="form_menu_B",text="SHOOT",font="Verdana",font_size=30,font_color=constantes.C_WHITE)
       
        self.widget_list = [self.boton1,self.boton2,self.boton_shoot]

        self.life_bar = pygame.image.load("images/assets/vida.png")
        self.life_line = pygame.image.load("images/assets/vida_verde_2.png")
        self.font = pygame.font.Font(None, 24)

        # --- GAME ELEMNTS --- 
        self.static_background = Background(x=0,y=0,width=w,height=h,path="images/locations/set_bg_01/forest/all.png")
        self.ground = pygame.Rect(0, constantes.GROUND_LEVEL,constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA -  constantes.GROUND_LEVEL)
        self.bullet_list = []

        self.enemy_list = [EnemyFactory.get_ogre_enemy(450,400,self), EnemyFactory.get_ogre_enemy(900, 400, self)]

        self.platform_list = PlatformFactory.get_platforms_for_level(constantes.LEVEL_1)

        self.has_won = False
        self.is_paused = False
        self.consumable_list = []
        
        self.player_list = []

    @abstractmethod
    def create_player(self):
        pass
    
    @abstractmethod
    def create_victory(self):
        pass

    def update(self, lista_eventos,keys,delta_ms, player_list):
        self.check_victory()
        if not self.freeze():
            self.update_consumables(delta_ms, self.platform_list, player_list)
            for aux_widget in self.widget_list:
                aux_widget.update(lista_eventos)
                
            for bullet_element in self.bullet_list:
                bullet_element.update(delta_ms,self.platform_list,self.enemy_list,player_list)

            for enemy_element in self.enemy_list:
                enemy_element.update(delta_ms,self.platform_list, player_list)
    
    def update_consumables(self, delta_ms, platform_list, player_list):
        self.create_consumable()
        for consumable in self.consumable_list:
            consumable.update(delta_ms, platform_list)
            consumable.check_picked_up(player_list)

    def create_consumable(self):
        if self.must_create_consumable():
            self.consumable_list.append(self.get_random_consumable())

    def must_create_consumable(self):
        actual_time = pygame.time.get_ticks()
        can_create = False
        if actual_time - self.last_consumable_time > self.consumable_time_interval:
            self.last_consumable_time = actual_time
            can_create = True
        return len(self.consumable_list) < 3 and can_create

    def get_coords_for_new_consumable(self):
        return random.randint(15, constantes.ANCHO_VENTANA - 15),random.randint(15, self.ground.top - 5)
    
    def get_random_consumable(self):
        # number = random.randint(1,100)
        # if number <= 25:
            x,y = self.get_coords_for_new_consumable()
            return HealthConsumable(x,y,self, 10)

    def destroy_consumable(self, consumable):
        self.consumable_list.remove(consumable)
    
    def draw(self): 
        
        # self.draw_ground()
        super().draw()
        screen = self.surface
        self.static_background.draw(self.surface)

        for plataforma in self.platform_list:
            plataforma.draw(self.surface)

        for enemy_element in self.enemy_list:
            enemy_element.draw(self.surface)

        for bullet_element in self.bullet_list:
            bullet_element.draw(self.surface)
        
        for consumable in self.consumable_list:
            consumable.draw(screen)

        self.draw_life_bars(screen)

        
    
    def draw_life_bars(self, screen):
        y = 5
        for index, player in enumerate(self.player_list):
            number_text = self.font.render(str(index + 1), True, (255, 255, 255)) 
            text_pos = (5, y + (self.life_bar.get_height() / 3))
            screen.blit(number_text, text_pos)
            screen.blit(self.life_bar, (15, y))
            for life_line in range(player.lives):
                screen.blit(self.life_line, (life_line + 16, y + 1))
            y += self.life_bar.get_height() + 3
    
    def draw_ground(self):
        pygame.draw.rect(self.surface, (0,0,0,0), self.ground)

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
    
    def player_can_update(self, player):
        return not player.is_dead and not self.freeze()
    
    def freeze(self):
        return self.has_won or self.is_paused
    
    def on_click_shoot(self, parametro):
        constantes.toggle_debug()
        # for enemy_element in self.enemy_list:
        #     self.bullet_list.append(Bullet(enemy_element,enemy_element.rect.centerx,enemy_element.rect.centery,self.player_1.rect.centerx,self.player_1.rect.centery,20,path="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",frame_rate_ms=100,move_rate_ms=20,width=5,height=5))

