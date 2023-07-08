

from gui.gui_form import Form


class Level(Form):
    levels_dict = {}
    def __init__(self, name, master_surface, x, y, w, h, color_background, color_border, active):
        super().__init__(name, master_surface, x, y, w, h, color_background, color_border, active)
        Level.levels_dict[name] = self
        self.consumable_time_interval = 1000
        self.last_consumable_time = 0
        