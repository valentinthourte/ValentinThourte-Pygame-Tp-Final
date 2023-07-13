
import pygame
from collision_helper import CollisionHelper
from db_helper import DBHelper
from gui.gui_form import Form
import constantes
from gui.gui_button import Button


class Level(Form):
    level_dict = {}
    player_list = []
    player_names = []
    clean_level = None
    def __init__(self, name, master_surface, x, y, w, h, color_background, color_border, active):
        super().__init__(name, master_surface, x, y, w, h, color_background, color_border, active)
        Level.level_dict[name] = self
        self.consumable_time_interval = 1000
        self.last_consumable_time = 0
        self.interactable_list = []
        self.lost = False

        self.widget_list = []


    def check_use(self, player):
        for element in self.interactable_list:
            if CollisionHelper.player_colliding_with_entity(player, element):
                element.use(self, player)
    
    def check_loss(self):
        lost = True
        for player in Level.player_list:
            if not player.died():
                lost = False
        self.lost = lost

    def restart(self):
        Level.player_list = []

    @staticmethod
    def update_player_names(name_list):
        for name, player in zip(name_list, Level.player_list):
            player.set_name(name)

    @staticmethod
    def add_score_to_players(score):
        Level.update_player_names(Level.player_names)
        for player in Level.player_list:
            player.increase_score(score)

    @staticmethod
    def quit(param):
        for player in Level.player_list:
            DBHelper.set_score_for_player(player=player)
        scores = DBHelper.get_scores()
        for score in scores:
            print(score)
        Form.quit(param)

    @staticmethod
    def get_next_level_name():
        active_level = Level.get_active_level()
        if active_level:
            match active_level:
                case constantes.NAME_LEVEL_1:
                    return Form.selected_type.format(["2"])
                case constantes.NAME_LEVEL_2:
                    return Form.selected_type.format(["3"])
        else:
            return Form.selected_type.format(["1"])

    @staticmethod
    def get_active_level():
        for level in Level.level_dict:
            if Level.level_dict[level].active:
                return level

    @staticmethod
    def update_players(level):  
        for player in Level.player_list:
            player.owner = level
            player.reset()
    
    def update(self, lista_eventos):
        for aux_widget in self.widget_list:
            aux_widget.update(lista_eventos)
    
    def draw(self):
        super().draw()
        for aux_widget in self.widget_list:
            aux_widget.draw() 
    
    