import pygame
from collision_helper import CollisionHelper
from constantes import *
from fallable import Fallable

class Consumable(Fallable):
    # Clase CONSUMABLE
    # Utilizada para encapsular la lógica correspondiente a entidades consumibles, es decir, que colisionan con un jugador y surten un efecto sobre el mismo.
    # Contiene lógica para determinar si fue consumida (si un jugador colisionó), para eliminarse una vez que su efecto fue surtido
    # Esta clase también hereda de Fallable, el cual se encarga de aplicar gravedad y colisión con el suelo a las entidades
    # También contiene lógica para el movimiento tipo flotación cuando queda en contacto con el suelo
    
    def __init__(self, x, y, image_path, w, h, owner, scale=True,frame_rate_ms = 100,move_rate_ms = 50, float_height = 10) -> None:
        Fallable.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        if scale:
            self.image = pygame.transform.scale(self.image, (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
        Fallable.create_ground_collition_rect(self)
        self.owner = owner
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.float_height = float_height
        self.float_interval = 25
        self.last_float_time = 0
        self.going_up = True
        self.contacting_platform = None
    
    def check_picked_up(self, player_list):
        for player in player_list:
            if CollisionHelper.player_colliding_with_entity(player, self):
                player.picked_up(self)
    
    def effect(self, player):
        self.destroy()
    
    def destroy(self):
        self.owner.destroy_consumable(self)
    
    def draw(self, screen):
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
        Fallable.draw(self, screen)
        screen.blit(self.image,self.rect)
    
    def update(self, delta_ms, plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        if not self.is_grounded:
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
        if self.contacting_platform.top - self.rect.bottom >= self.float_height:
            self.going_up = False
        elif self.rect.bottom >= self.contacting_platform.top:
            self.going_up = True
    
    def change_y(self,delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y
    
    def update_grounded(self, platform_list):
        was_grounded = self.is_grounded
        super().update_grounded(platform_list)
        self.is_grounded = self.is_grounded or CollisionHelper.consumable_must_float(self, self.owner.ground)
        if self.is_grounded != was_grounded:
            self.contacting_platform = CollisionHelper.get_contacting_platform_for_entity(self, platform_list, self.owner)
            if not self.contacting_platform:
                self.is_grounded = False
