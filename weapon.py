from constantes import *

class Weapon():
    def __init__(self, owner, damage = 1) -> None:
        self.default_damage = damage
        self.damage = damage
        self.owner = owner
    
    def shoot(self):
        pass

    def increase_damage(self, percent):
        self.damage = self.damage + self.damage * (percent / 100)
    
    def reset_damage(self):
        self.damage = self.default_damage
    
    def get_bullet_end_coords_from_direction(self, direction):
        coords = [0, self.owner.rect.centery]
        if direction == DIRECTION_R:
            coords[0] = ANCHO_VENTANA
        return coords
