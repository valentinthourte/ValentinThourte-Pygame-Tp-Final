import pygame
import constantes  
from auxiliar import Auxiliar


class Plataform:
    def __init__(self, x, y,width, height,  type=1):

        self.image_list= Auxiliar.getSurfaceFromSeparateFiles("images/tileset/forest/Tiles/{0}.png",1,18,flip=False,w=width,h=height)
        self.type  = type
        self.image = self.image_list[type]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(self.rect)
        self.ground_collition_rect = pygame.Rect(self.rect)
        self.ground_collition_rect.height = constantes.GROUND_COLLIDE_H

    def draw(self,screen):
        screen.blit(self.image,self.rect)
        if(constantes.DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
    
    def update(self):
        pass
        

class MovingPlatform(Plataform):
    def __init__(self, x, y, width, height, type=1, move_distance = 100, move_speed = 2, starting_direction = constantes.DIRECTION_R):
        super().__init__(x, y, width, height, type)
        self.start_x = x
        self.end_x = x + move_distance

        self.move_speed = move_speed
        self.direction = starting_direction

    @classmethod
    def from_parent(cls, parent_instance, move_distance=100, move_speed=2, starting_direction=constantes.DIRECTION_R):
        return cls(parent_instance.rect.x, parent_instance.rect.y, parent_instance.rect.width, parent_instance.rect.height, parent_instance.type, move_distance, move_speed, starting_direction)

    def update(self):
        match self.direction:
            case constantes.DIRECTION_R:
                if self.rect.x >= self.end_x:
                    self.toggle_direction()
            case constantes.DIRECTION_L:
                if self.rect.x <=  self.start_x:
                    self.toggle_direction()
        self.change_x()

    def change_x(self):
        self.rect.x += self.move_speed
        self.collition_rect.x += self.move_speed
        self.ground_collition_rect.x += self.move_speed
    
    def toggle_direction(self):
        direction = constantes.DIRECTION_R
        if self.direction == constantes.DIRECTION_R:
            direction = constantes.DIRECTION_L
        self.direction = direction
        self.move_speed = -self.move_speed
        

        