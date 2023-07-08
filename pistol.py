
from constantes import *
from bullet import Bullet
from weapon import Weapon


class Pistol(Weapon):
    def __init__(self, owner, damage=1) -> None:
        super().__init__(owner, damage)
    
    def shoot(self, direction):
        bullet_end_coords = self.get_bullet_end_coords_from_direction(direction)
        bullet_x_end = bullet_end_coords[0]
        bullet_y_end = bullet_end_coords[1]
        return Bullet(self.owner,self.owner.rect.centerx,self.owner.rect.centery,bullet_x_end,bullet_y_end,20,path=PATH_USER_BULLET,frame_rate_ms=100,move_rate_ms=20, flip= direction == DIRECTION_L,width=32,height=32)
    
    def get_bullet_end_coords_from_direction(self, direction):
        coords = [0, self.owner.rect.centery]
        if direction == DIRECTION_R:
            coords[0] = ANCHO_VENTANA
        return coords