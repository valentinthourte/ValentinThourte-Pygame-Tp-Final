import pygame
from pygame.locals import *
from boss import Boss
from constantes import *
from gui.gui_form import Form
from gui.gui_button import Button
from gui.gui_textbox import TextBox
from gui.gui_progressbar import ProgressBar
from gui.gui_factory import GuiFactory
from levels.L2.gui_form_menu_game_l2 import FormGameLevel2
from levels.level import Level
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from collision_helper import CollisionHelper
from victory import Victory
from player_factory import PlayerFactory
from gui.widget_factory import WidgetFactory

class FormGameLevel2_SP(FormGameLevel2):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)

        self.create_victory()
        self.added_score = False
        self.final_button = None
        self.can_activate_boss = False
        self.boss = None

        self.next_level_button = WidgetFactory.get_next_level_button(self,300,300, Form.selected_type.format(3))
    
    def create_victory(self):
        self.victory = Victory(self, SINGLEPLAYER_VICTORY_IMAGE_PATH, 88, 463, 1400, 0, 200)
        # self.victory = Victory(self, MULTIPLAYER_VICTORY_IMAGE_PATH, 88, 463, 1400, 0, 200, scale=False)

    def on_click_boton1(self, parametro):
        self.set_active(parametro)
        
    def update(self, lista_eventos,keys,delta_ms, player_list = None):

        if len(Level.player_list) > 0:
            self.player_1 = Level.player_list[0]

        if not player_list:
            player_list = Level.player_list

        super().update(lista_eventos,keys,delta_ms, player_list, self.boss)

        self.check_victory()

        if self.player_can_move(self.player_1):
            self.player_1.events(delta_ms,keys)
        self.player_1.update(delta_ms,self.platform_list)
        
        self.victory.update(delta_ms, plataform_list=self.platform_list)

        self.update_boss(delta_ms, player_list)

        if self.next_level_button:
            self.next_level_button.update(lista_eventos)


    def update_boss(self, delta_ms, player_list):
        if self.boss_is_active():
            if not self.boss:
                self.boss = self.create_boss()
                self.boss.activate()
            self.boss.update(delta_ms,self.platform_list, player_list)
        
    def boss_is_active(self):
        return len(self.enemy_list) <= 0 and self.can_activate_boss and not self.killed_boss
    
    def draw(self): 
        super().draw()
        self.player_1.draw(self.surface)
        
        if self.boss_is_active(): 
            self.boss.draw(screen=self.surface)

        if self.can_win:
            self.victory.draw(screen=self.surface)


    
    def get_colliding_enemies(self, player):
        colliding_enemy_list = []
        for enemy in self.enemy_list:
            if CollisionHelper.player_colliding_with_entity(player, enemy):
                colliding_enemy_list.append(enemy)
        return colliding_enemy_list
    
    
    def kill(self, enemy: Enemy):
        self.enemy_list.remove(enemy)

    def check_victory(self):
        self.check_can_win()
        if self.can_win:
            if CollisionHelper.player_colliding_with_entity(self.player_1, self.victory):
                self.has_won = True
                if self.victory.show_victory(self.surface):
                    self.show_won_screen()                    
                    if not self.added_score:
                        self.score += self.player_1.get_health()
                        Level.add_score_to_players(self.score)
                        self.added_score = True

    def show_won_screen(self):
        self.surface.fill(C_BLACK)
        img = pygame.image.load(START_IMAGE_PATH)
        x,y = self.slave_rect.center
        h = img.get_height() // 2
        w = img.get_width() // 2
        image_x = x - w // 2
        image_y = ALTO_VENTANA - h
        background = Background(image_x,image_y,w,h,START_IMAGE_PATH, True)
        background.draw(self.surface)

        font = pygame.font.Font(BLOOD_FONT_PATH, 100)
        
        text = "YOU WIN"
        title = font.render(text, True, C_GREEN)     
        text_width = title.get_width()
        title_x = self.slave_rect.centerx - text_width // 2
        title_y = 100
        score_text = f"Score: {self.player_1.score}"
        score_x = title_x
        score_y = 500
        font = pygame.font.Font(BLOOD_FONT_PATH, 60)
        score = font.render(score_text, (score_x, score_y), C_RED)
        self.master_surface.blit(title, (title_x, title_y))
        self.master_surface.blit(score, (score_x, score_y))
        self.next_level_button.draw()
        

    def check_can_win(self):
        self.can_win = len(self.enemy_list) == 0 and self.killed_boss

    def get_sender_params(self):
        return {
            "score": self.player_1.score,
            "next": "2"
        }

    
    def freeze(self):
        return self.has_won