from player import *
from constantes import *
from auxiliar import Auxiliar
from particle import ParticleList
from collision_helper import CollisionHelper
from animatable import Animatable
from killable import Killable

class Enemy(Animatable, Killable):
    
    def __init__(self,x,y,speed_walk,speed_run,gravity,jump_power,frame_rate_ms,move_rate_ms,jump_height, owner,p_scale=1,interval_time_jump=100) -> None:
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",0,7,scale=p_scale)
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",0,7,flip=True,scale=p_scale)
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",0,7,scale=p_scale)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",0,7,flip=True,scale=p_scale)
        self.knife_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/ATTAK/ATTAK_00{0}.png",0,7,scale=p_scale)
        self.knife_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/ATTAK/ATTAK_00{0}.png",0,7,flip=True,scale=p_scale)
        self.die = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",0,6,scale=p_scale)
        
        self.contador = 0
        self.frame = 0
        self.lives = 5
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk =  speed_walk
        self.speed_run =  speed_run
        self.gravity = gravity
        self.jump_power = jump_power
        self.animation = self.stay_r
        self.direction = DIRECTION_R
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H

        self.is_jump = False
        self.is_fall = False
        self.is_shoot = False
        self.is_knife = False
        self.is_dead = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0 # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump

        self.particle_list = ParticleList(self)

        self.owner = owner
   
    def change_x(self,delta_x):
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self,delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def do_movement(self,delta_ms,plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0

            if(not self.is_on_plataform(plataform_list)):
                if(self.move_y == 0):
                    self.is_fall = True
                    self.change_y(self.gravity)
            else:
                self.is_fall = False
                self.change_x(self.move_x)
                if self.contador <= 50:
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l
                    self.direction = DIRECTION_L
                    self.contador += 1 
                elif self.contador <= 100:
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                    self.direction = DIRECTION_R
                    self.contador += 1
                else:
                    self.contador = 0
    
    def is_on_plataform(self,plataform_list):
        retorno = False
        
        if(self.ground_collition_rect.bottom >= GROUND_LEVEL):
            retorno = True     
        else:
            for plataforma in  plataform_list:
                if(self.ground_collition_rect.colliderect(plataforma.ground_collition_rect)):
                    retorno = True
                    break       
        return retorno          

    def do_animation(self,delta_ms):
        if self.is_dead and self.animation_ended():
            print("Enemy dead and animation ended.")
            self.owner.kill(self)
        else:
            if self.is_dead:
                self.animation = self.die
            self.tiempo_transcurrido_animation += delta_ms
            if(self.tiempo_transcurrido_animation >= self.frame_rate_ms):
                self.tiempo_transcurrido_animation = 0
                if(not self.animation_ended()):
                    self.frame += 1 
                else: 
                    self.frame = 0

    def update(self,delta_ms,plataform_list, player):
        if not self.died():
            self.do_movement(delta_ms,plataform_list)
            self.check_collision(player)
        
        self.do_animation(delta_ms) 

    def draw(self,screen):
        
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
        
        self.image = self.animation[self.frame]
        screen.blit(self.image,self.rect)
        self.particle_list.show_particles(screen)

    def receive_shoot(self) -> bool:
        self.lives -= 1
        self.particle_list.create_hit_particle()
        if self.lives <= 0:
            self.is_dead = True            
            self.frame = 0
            self.animation = self.die
    
    def check_collision(self, player):
        if CollisionHelper.player_colliding_with_entity(player, self):
            self.animation = self.get_animation_by_direction()
            if not self.is_knife:
                self.is_knife = True
                player.receive_shoot()
        else:
            self.is_knife = False
            
    def get_animation_by_direction(self):
        animation = self.knife_l
        if self.direction == DIRECTION_R:
            animation = self.knife_r
        return animation
