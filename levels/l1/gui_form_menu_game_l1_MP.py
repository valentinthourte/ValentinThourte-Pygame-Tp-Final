import pygame
from pygame.locals import *
from constantes import *
from gui.gui_form import Form
from gui.gui_button import Button
from gui.gui_textbox import TextBox
from gui.gui_progressbar import ProgressBar
from levels.l1.gui_form_menu_game_l1 import FormGameLevel1
from levels.level import Level
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from bullet import Bullet
from collision_helper import CollisionHelper
from player_factory import PlayerFactory
from victory import Victory
from gui.widget_factory import WidgetFactory

class FormGameLevel1_MP(FormGameLevel1):
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        super().__init__(name,master_surface,x,y,w,h,color_background,color_border,active)
        self.create_victory()
        self.added_score = False
        self.next_level_button = WidgetFactory.get_next_level_button(self,300,300, Form.selected_type.format(2))

    def create_player(self):
        id_player_1 = 1
        id_player_2 = 2
        
        self.player_1 = PlayerFactory.get_player(1, 30, 400 ,self, PATH_COWGIRL_IMAGES, PLAYER_1_KEYS)
        self.player_2 = PlayerFactory.get_player(2, 60, 400 ,self, PATH_COWBOY_IMAGES, PLAYER_2_KEYS)
        
        self.player_key_list = {id_player_1: PLAYER_1_KEYS, id_player_2: PLAYER_2_KEYS}
        Level.player_list = [self.player_1, self.player_2]
    
    def create_victory(self):
        # self.victory = Victory(MULTIPLAYER_VICTORY_IMAGE_PATH, 88, 463, 1400, 137, 200)
        self.victory = Victory(self, SINGLEPLAYER_VICTORY_IMAGE_PATH, 88, 463, 1400, 137, 200)

    def on_click_boton1(self, parametro):
        self.set_active(parametro)

    def on_click_shoot(self, parametro):
        for enemy_element in self.enemy_list:
            self.bullet_list.append(Bullet(enemy_element,enemy_element.rect.centerx,enemy_element.rect.centery,self.player_1.rect.centerx,self.player_1.rect.centery,20,path="images/gui/set_gui_01/Comic_Border/Bars/Bar_Segment05.png",frame_rate_ms=100,move_rate_ms=20,width=5,height=5))

    def update(self, lista_eventos,keys,delta_ms, player_list = None):
        if len(Level.player_list) == 0:
            self.create_player()
        if not player_list:
            player_list = Level.player_list

        super().update(lista_eventos,keys,delta_ms, player_list)

        self.check_victory()
        for player in Level.player_list:
            if self.player_can_move(player):
                player.events(delta_ms,keys)
            player.update(delta_ms,self.platform_list)
        self.victory.update(delta_ms, plataform_list=self.platform_list)
        if self.next_level_button:
            self.next_level_button.update(lista_eventos)
        if self.loss_button:
            self.loss_button.update(lista_eventos)
    
    def check_victory(self):
        self.check_can_win()
        if self.can_win:
            if CollisionHelper.player_colliding_with_entity(self.player_1, self.victory):
                self.has_won = True
                if self.victory.show_victory(self.surface):
                    self.show_won_screen()                    
                    if not self.added_score:
                        Level.add_score_to_players(self.score)
                        self.added_score = True

    def show_won_screen(self):
        self.surface.fill(C_BLACK)
        img = pygame.image.load(START_IMAGE_PATH)
        x,y = self.slave_rect.center
        h = img.get_height() // 2
        w = img.get_width() // 2
        image_x = x - w
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
        self.can_win = len(self.enemy_list) == 0 

    def draw(self): 
        super().draw()
    
        for player in Level.player_list:
            player.draw(self.surface)
        
        self.victory.draw(screen=self.surface)
    
    def players_have_won(self):
        have_won = True
        for player in Level.player_list:
            if not CollisionHelper.player_colliding_with_entity(player, self.victory):
                have_won = False
        return have_won
    

    