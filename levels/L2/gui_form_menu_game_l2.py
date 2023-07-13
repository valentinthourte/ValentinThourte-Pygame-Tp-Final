from boss import Boss
from button_interactable import ButtonInteractable
from damage_consumable import DamageConsumable
from moving_background import MovingBackground
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
from plataforma import MovingPlatform, Plataform
from background import Background
from collision_helper import CollisionHelper
from victory import Victory
from abc import ABC, abstractmethod
from enemy_factory import EnemyFactory
from platform_helper import PlatformHelper
from gui.widget_factory import WidgetFactory


class FormGameLevel2(Level):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)

        

        # --- GUI WIDGET --- 
        self.reload_platforms_button = Button(master=self,x=300,y=10,w=140,h=50,color_background=None,color_border=None,image_background="images/gui/set_gui_01/Comic_Border/Buttons/Button_M_02.png",on_click=self.reload_platforms,on_click_param="form_menu_B",text="Reload Platforms",font="Verdana",font_size=30,font_color=constantes.C_WHITE)

        self.widget_list = [self.reload_platforms_button]

        self.life_bar = pygame.image.load("images/assets/vida.png")
        self.life_line = pygame.image.load("images/assets/vida_verde_2.png")
        self.font = pygame.font.Font(None, 24)

        # --- GAME ELEMNTS --- 
        self.background = self.create_background()
        self.static_background = Background(x=0,y=0,width=w,height=h,path=constantes.LEVEL_2_BACKGROUND)
        self.ground = pygame.Rect(0, constantes.GROUND_LEVEL,constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA -  constantes.GROUND_LEVEL)
        self.bullet_list = []
        self.loss_button = None


        self.score = 0
        
        self.killed_boss = False

        self.create_enemies()
        self.platform_list = PlatformHelper.get_platforms_for_level(constantes.LEVEL_2)

        self.has_won = False
        self.can_win = False
        self.is_paused = False
        self.consumable_list = [DamageConsumable(1200,300,self,20)]
        self.max_consumable_amount = 10
        self.consumable_count = 0
        self.enemy_count = 0
        self.interactable_list.append(ButtonInteractable(1345,80,32,32,self,scale=False))
        self.must_update_players = True


    def create_boss(self):
        boss_x = 800
        boss_y = 300
        return Boss(boss_x,boss_y,self, constantes.LEVEL_2_BOSS_IMG, 100,50,600,False, 75, image_scale=0.3)
    
    def create_enemies(self):
        self.enemy_list = []
        for i in range(7):
            x,y = self.get_coords_for_new_entity()
            self.enemy_list.append(EnemyFactory.get_ogre_enemy(x,y,self,is_active=i <= 2, health=150))

    def reload_platforms(self,param):
        print("Reloading platforms")
        self.platform_list = PlatformHelper.get_platforms_for_level(constantes.LEVEL_2)

    @abstractmethod
    def create_player(self):
        pass
    
    @abstractmethod
    def create_victory(self):
        pass

    def create_background(self):
        return MovingBackground(constantes.LEVEL_1_BACKGROUND, self.surface, 3, 4)
    
    def kill_boss(self, boss):
        self.killed_boss = True
        boss.is_active = False
        self.score += 30

    def update(self, lista_eventos,keys,delta_ms, player_list, boss):
        if self.must_update_players:
            Level.update_players(self)
            self.must_update_players = False
        if not self.freeze():
            self.update_consumables(delta_ms, self.platform_list, player_list)
            self.update_enemies(delta_ms,player_list)
            for platform in self.platform_list:
                platform.update()
            for aux_widget in self.widget_list:
                aux_widget.update(lista_eventos)
                
            for bullet_element in self.bullet_list:
                bullet_element.update(delta_ms,self.platform_list,self.enemy_list,player_list, boss)
            
            for interactable in self.interactable_list:
                interactable.update(player_list)
                
        if not self.lost:
            self.check_loss()
        else:
            self.show_loss_screen()
            if self.loss_button:
                self.loss_button.update(lista_eventos)

    def show_loss_screen(self):
        self.surface.fill(constantes.C_BLACK)
        img = pygame.image.load(constantes.START_IMAGE_PATH)
        x,y = self.slave_rect.center
        h = img.get_height() // 2
        w = img.get_width() // 2
        image_x = x - w
        image_y = constantes.ALTO_VENTANA - h
        background = Background(image_x,image_y,w,h,constantes.START_IMAGE_PATH, True)
        background.draw(self.surface)

        font = pygame.font.Font(constantes.BLOOD_FONT_PATH, 100)
        
        text = "YOU LOSE"
        title = font.render(text, True, constantes.C_RED)     
        text_width = title.get_width()
        title_x = self.slave_rect.centerx - text_width // 2
        title_y = 100
        score_text = f"Score: {self.player_1.score}"
        score_x = title_x
        score_y = 500
        font = pygame.font.Font(constantes.BLOOD_FONT_PATH, 60)
        score = font.render(score_text, (score_x, score_y), constantes.C_RED)
        self.master_surface.blit(title, (title_x, title_y))
        self.master_surface.blit(score, (score_x, score_y))
        if not self.loss_button:
            self.loss_button = WidgetFactory.get_restart_button(self,300,300, function=Form.restart_form, parameter=self.name)
        self.loss_button.draw()

    def update_enemies(self,delta_ms, player_list):
        self.create_enemy_if_needed()
        for enemy_element in self.enemy_list:
            enemy_element.update(delta_ms,self.platform_list, player_list)


    def create_enemy_if_needed(self):
        if len(self.active_enemies()) < 3 and self.enemy_count < 7:
            self.activate_enemy()

    def activate_enemy(self):
        for index,enemy in enumerate(self.enemy_list):
            if not enemy.active():
                self.enemy_list[index].activate()
                break
            
    def active_enemies(self):
        active_list = []
        for enemy in self.enemy_list:
            if enemy.is_active:
                active_list.append(enemy)
        return active_list

    def update_consumables(self, delta_ms, platform_list, player_list):
        self.create_consumable()
        for consumable in self.consumable_list:
            consumable.update(delta_ms, platform_list)
            consumable.check_picked_up(player_list)

    def create_consumable(self):
        if self.must_create_consumable():
            self.consumable_count += 1
            self.consumable_list.append(self.get_random_consumable())

    def must_create_consumable(self):
        actual_time = pygame.time.get_ticks()
        can_create = False
        if actual_time - self.last_consumable_time > self.consumable_time_interval:
            self.last_consumable_time = actual_time
            can_create = True
        return len(self.consumable_list) < 3 and can_create and self.max_consumable_amount > self.consumable_count

    def get_coords_for_new_entity(self):
        return random.randint(15, constantes.ANCHO_VENTANA - 15),random.randint(15, self.ground.top - 5)
    
    def get_random_consumable(self):
        # number = random.randint(1,100)
        # if number <= 25:
            x,y = self.get_coords_for_new_entity()
            return HealthConsumable(x,y,self, 10)

    def destroy_consumable(self, consumable):
        self.consumable_list.remove(consumable)
        self.score += 1
    
    def draw(self): 
        if constantes.DEBUG:
            self.draw_ground()
        
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
        
        for interactable in self.interactable_list:
            interactable.draw(screen)
            
        for aux_widget in self.widget_list:
            aux_widget.draw() 

        self.draw_life_bars(screen)

        
    
    def draw_life_bars(self, screen):
        y = 5
        for index, player in enumerate(Level.player_list):
            number_text = self.font.render(str(index + 1), True, (255, 255, 255)) 
            text_pos = (5, y + (self.life_bar.get_height() / 3))
            screen.blit(number_text, text_pos)
            screen.blit(self.life_bar, (15, y))
            for life_line in range(player.lives):
                screen.blit(self.life_line, (life_line + 16, y + 1))
            y += self.life_bar.get_height() + 3
    
    def draw_ground(self):
        pygame.draw.rect(self.surface, (255,255,255), self.ground)

    def player_shoot(self, bullet):
        self.bullet_list.append(bullet)

    def boss_shoot(self,bullet):
        self.bullet_list.append(bullet)
    
    def get_colliding_enemies(self, player):
        colliding_enemy_list = []
        for enemy in self.enemy_list:
            if CollisionHelper.player_colliding_with_entity(player, enemy):
                colliding_enemy_list.append(enemy)
        return colliding_enemy_list
    
    
    def kill_enemy(self, enemy: Enemy):
        self.enemy_list.remove(enemy)
        self.enemy_count += 1
        self.score += 1
    
    def player_can_move(self, player):
        return not player.is_dead and not self.freeze()
    
    def freeze(self):
        return self.has_won or self.is_paused
    
    def on_click_shoot(self, parametro):
        constantes.toggle_debug()
        # for enemy_element in self.enemy_list:
        #     self.bullet_list.append(Bullet(enemy_element,enemy_element.rect.centerx,enemy_element.rect.centery,self.player_1.rect.centerx,self.player_1.rect.centery,20,path="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",frame_rate_ms=100,move_rate_ms=20,width=5,height=5))

