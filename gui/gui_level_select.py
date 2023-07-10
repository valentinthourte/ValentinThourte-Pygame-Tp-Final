

from gui.gui_form import Form


class FormLevelSelect(Form):
    def __init__(self, name, master_surface, x, y, w, h, color_background, color_border, active):
        super().__init__(name, master_surface, x, y, w, h, color_background, color_border, active)

        