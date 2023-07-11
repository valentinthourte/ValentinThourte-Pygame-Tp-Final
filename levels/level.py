

from collision_helper import CollisionHelper
from gui.gui_form import Form
import constantes


class Level(Form):
    level_dict = {}
    player_list = []
    clean_level = None
    def __init__(self, name, master_surface, x, y, w, h, color_background, color_border, active):
        super().__init__(name, master_surface, x, y, w, h, color_background, color_border, active)
        Level.level_dict[name] = self
        self.consumable_time_interval = 1000
        self.last_consumable_time = 0
        self.interactable_list = []
        self.lost = False

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
            player.reset_coords()

    
    