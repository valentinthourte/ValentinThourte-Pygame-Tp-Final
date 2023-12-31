from constantes import *
import math
from collision_helper import CollisionHelper

class Bullet():
    
    def __init__(self,owner,x_init,y_init,x_end,y_end,speed,path,frame_rate_ms,move_rate_ms, flip, width=5,height=5, damage = 1) -> None:
        self.tiempo_transcurrido_move = 0
        self.tiempo_transcurrido_animation = 0
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(width,height))
        self.image = pygame.transform.flip(self.image, flip, False)
        self.rect = self.image.get_rect()
        self.x = x_init
        self.y = y_init
        self.owner = owner
        self.rect.x = x_init
        self.rect.y = y_init
        self.collition_rect = self.rect
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        angle = math.atan2(y_end - y_init, x_end - x_init) #Obtengo el angulo en radianes
        self.damage = damage

        self.move_x = math.cos(angle)*speed
        self.move_y = math.sin(angle)*speed
        
        self.is_active = True 
    
    def change_x(self,delta_x):
        self.x = self.x + delta_x
        self.rect.x = int(self.x)   

    def change_y(self,delta_y):
        self.y = self.y + delta_y
        self.rect.y = int(self.y)

    def do_movement(self,delta_ms,plataform_list,enemy_list,player, boss = None):
        self.tiempo_transcurrido_move += delta_ms
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0
            self.change_x(self.move_x)
            self.change_y(self.move_y)
            self.check_impact(plataform_list,enemy_list,player, boss)

    def do_animation(self,delta_ms):
        self.tiempo_transcurrido_animation += delta_ms
        if(self.tiempo_transcurrido_animation >= self.frame_rate_ms):
            self.tiempo_transcurrido_animation = 0
            pass
    
    def check_impact(self,plataform_list,enemy_list,player_list, boss):
        if boss and self.owner == boss.weapon:
            self.check_player_impact(player_list)
            pygame.transform.rotate(self.image, 5)
        else:
            self.check_enemy_impact(enemy_list)
            self.check_platform_impact(plataform_list)
            if boss:
                self.check_boss_impact(boss)
        if self.rect.x <= 0 or self.rect.x >= ANCHO_VENTANA:
            self.is_active = False

        
    def check_boss_impact(self, boss):
        if self.is_active and CollisionHelper.entities_colliding(self, boss):
            boss.receive_shoot(self.damage)
            self.is_active = False

    def check_platform_impact(self, platform_list):
        for platform in platform_list:
            if self.is_active and CollisionHelper.entities_colliding(self, platform):
                print("IMPACTO PLATAFORMA")
                self.is_active = False

    def check_enemy_impact(self, enemy_list):
        for aux_enemy in enemy_list:
            if(self.is_active and self.owner != aux_enemy and CollisionHelper.entities_colliding(self, aux_enemy) and not aux_enemy.died()):
                aux_enemy.receive_shoot(self.damage)
                self.is_active = False

    def check_player_impact(self, player_list):
        for player in player_list:
            if(self.is_active and self.owner != player and CollisionHelper.player_colliding_with_entity(player, self) and not player.died()):
                player.receive_shoot(self.damage)
                self.is_active = False

    def update(self,delta_ms,plataform_list,enemy_list,player, boss = None):
        self.do_movement(delta_ms,plataform_list,enemy_list,player, boss)
        
        self.do_animation(delta_ms) 

    def draw(self,screen):
        if(self.is_active):
            if(DEBUG):
                pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            screen.blit(self.image,self.rect)
