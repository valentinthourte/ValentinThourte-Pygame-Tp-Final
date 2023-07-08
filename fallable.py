from collision_helper import CollisionHelper
from constantes import *

class Fallable():
    def __init__(self):
        self.velocity_y = 0
        self.acceleration_y = 0
        self.is_grounded = True
        self.jumped = False
        
    
    def update_gravity(self):
        if (self.jumped or not self.is_grounded):
            if self.can_keep_accelerating():
                self.acceleration_y = GRAVITY_SPEED
                self.velocity_y += self.acceleration_y
        else:
            self.acceleration_y = 0
            self.velocity_y = 0
            
    def can_keep_accelerating(self):
        return self.velocity_y < TERMINAL_VELOCITY
    
    def is_on_plataform(self,plataform_list):
        retorno = False
    
        if(CollisionHelper.entity_is_grounded(self, self.owner) or CollisionHelper.entity_will_collide_with_ground(self)):
            retorno = True     
        else:
            for plataforma in plataform_list:
                if(CollisionHelper.fallable_colliding_with_entity(self, plataforma) or CollisionHelper.fallable_will_collide_with_entity(self, plataforma)):
                    retorno = True
                    break       
        return retorno   

    def update_grounded(self, platform_list):
        self.is_grounded = self.is_on_plataform(platform_list)

