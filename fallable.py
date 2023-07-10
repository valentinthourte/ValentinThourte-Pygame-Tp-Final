from collision_helper import CollisionHelper
from constantes import *
from particle import ParticleList

class Fallable():
    def __init__(self):
        self.velocity_y = 0
        self.acceleration_y = 0
        self.is_grounded = False
        self.jumped = False
        self.fall_particle_list = ParticleList(self) 
        
    
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
        was_grounded = self.is_grounded
        self.is_grounded = self.is_on_plataform(platform_list)
        if was_grounded != self.is_grounded and was_grounded == False:
            self.fall_particle_list.create_fall_particles()

    def draw(self, screen):
        self.fall_particle_list.show_particles(screen)

    @staticmethod
    def create_ground_collition_rect(entity):
        entity.ground_collition_rect = pygame.Rect(entity.collition_rect)
        entity.ground_collition_rect.height = GROUND_COLLIDE_H
        entity.ground_collition_rect.y = entity.collition_rect.bottom - GROUND_COLLIDE_H


