import pygame
from collision_helper import CollisionHelper
from constantes import *
from fallable import Fallable

class Consumable(Fallable):
    def __init__(self, x, y, image_path, w, h, owner, frame_rate_ms = 100,move_rate_ms = 50, float_height = 10) -> None:
        Fallable.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H
        self.owner = owner
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.float_height = float_height
        self.float_interval = 25
        self.last_float_time = 0
        self.going_up = True
    
    def check_picked_up(self, player_list):
        for player in player_list:
            if CollisionHelper.player_colliding_with_entity(player, self):
                player.picked_up(self)
    
    def effect(self, player):
        self.owner.destroy_consumable(self)
    
    def draw(self, screen):
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
        screen.blit(self.image,self.rect)
    
    def update(self, delta_ms, plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        self.update_grounded(plataform_list)
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0
            super().update_gravity()
            if self.is_grounded:
                self.update_floating()
            self.change_y(self.velocity_y)

    def update_floating(self):
        time = pygame.time.get_ticks()
        if time - self.last_float_time > self.float_interval:
            self.last_float_time = time
            self.update_float_direction()
            if self.going_up:
                self.velocity_y = -1
            else:
                self.velocity_y = 1

    
    def update_float_direction(self):
        if self.owner.ground.top - self.rect.y >= self.float_height:
            self.going_up = False
        elif self.rect.y >= self.owner.ground.top:
            self.going_up = True
    
    def change_y(self,delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y
    
    def update_grounded(self, platform_list):
        super().update_grounded(platform_list)
        self.is_grounded = self.is_grounded or CollisionHelper.consumable_must_float(self, self.owner.ground)
