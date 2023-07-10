from player import *
from constantes import *
from auxiliar import Auxiliar
from particle import ParticleList
from collision_helper import CollisionHelper
from animatable import Animatable
from killable import Killable
from attacker import Attacker
from fallable import Fallable
import random

class Enemy(Attacker, Animatable, Killable, Fallable):
    
    def __init__(self,x,y,speed_walk,speed_run,gravity,jump_power,frame_rate_ms,move_rate_ms,jump_height, owner,p_scale=1,interval_time_jump=100, lives = 100) -> None:
        Fallable.__init__(self)
        Attacker.__init__(self)
        Animatable.__init__(self)
        Killable.__init__(self, lives)

        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",0,7,scale=p_scale)
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/WALK/WALK_00{0}.png",0,7,flip=True,scale=p_scale)
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",0,7,scale=p_scale)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/IDLE/IDLE_00{0}.png",0,7,flip=True,scale=p_scale)
        self.knife_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/ATTAK/ATTAK_00{0}.png",0,7,scale=p_scale)
        self.knife_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/ATTAK/ATTAK_00{0}.png",0,7,flip=True,scale=p_scale)
        self.die = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/ork_sword/DIE/DIE_00{0}.png",0,6,scale=p_scale)
        
        self.contador = 0
        self.frame = 0
        self.lives = lives
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
        Fallable.create_ground_collition_rect(self)

        self.is_jump = False
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

    def toggle_direction(self):
        if self.direction == DIRECTION_R:
            self.move_x = -self.speed_walk
            self.animation = self.walk_l
            self.direction = DIRECTION_L
        else:
            self.move_x = self.speed_walk
            self.animation = self.walk_r
            self.direction = DIRECTION_R

    def switch_direction(self, direction):
        if direction == DIRECTION_R:
            self.direction = DIRECTION_L
            self.toggle_direction()
        else:
            self.direction = DIRECTION_R
            self.toggle_direction()
            

    
    def must_turn_direction(self):
        number = random.randint(1,100)
        return number <= 3 or CollisionHelper.is_against_edge(entity=self) 
    
    def choose_direction(self):
        number = random.randint(1,2)
        direction = DIRECTION_R
        if number == 1:
            direction = (DIRECTION_L)
        
        self.switch_direction(direction)

    def update_grounded(self, plataform_list):
        was_grounded = self.is_grounded
        super().update_grounded(plataform_list)
        if not was_grounded and self.is_grounded:
            self.choose_direction()

    def do_movement(self,delta_ms,plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        self.update_grounded(plataform_list)
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0

            self.update_gravity()

            self.change_x(self.move_x)
            self.change_y(self.velocity_y)
            
            if self.must_turn_direction():
                self.toggle_direction()

    def do_animation(self,delta_ms):
        if self.is_dead and self.animation_ended():
            self.owner.kill_enemy(self)
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

    def update(self,delta_ms,plataform_list, player_list):
        if not self.died():
            self.do_movement(delta_ms,plataform_list)
            self.check_collision(player_list)
        
        self.do_animation(delta_ms) 

    def draw(self,screen):
        
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
        Fallable.draw(self, screen)
        self.image = self.animation[self.frame]
        screen.blit(self.image,self.rect)
        self.particle_list.show_particles(screen)

    def receive_shoot(self, damage = 1) -> bool:
        self.lives -= damage 
        self.particle_list.create_hit_particle()
        if self.lives <= 0:
            self.is_dead = True            
            self.frame = 0
            self.animation = self.die
    
    def check_collision(self, player_list):
        for player in player_list:
            if CollisionHelper.player_colliding_with_entity(player, self) and not player.died():
                self.animation = self.get_attack_animation_by_direction()
                if not self.is_knife and self.can_shoot_again():
                    self.is_knife = True
                    player.receive_shoot(ENEMY_DAMAGE)
            else:
                self.is_knife = False
    
            
    def get_attack_animation_by_direction(self):
        animation = self.knife_l
        if self.direction == DIRECTION_R:
            animation = self.knife_r
        return animation
