

from animatable import Animatable
from attacker import Attacker
from auxiliar import Auxiliar
from collision_helper import CollisionHelper
from fallable import Fallable
from hammer import Hammer
from killable import Killable
from constantes import *
from particle import ParticleList

class Boss(Attacker,Killable, Animatable, Fallable):
    def __init__(self, x,y,owner,frame_rate_ms,move_rate_ms, lives, is_active):
        Attacker.__init__(self, BOSS_ATTACK_INTERVAL)
        Animatable.__init__(self)
        Killable.__init__(self, lives)
        Fallable.__init__(self)
        self.owner = owner


        self.load_animations()

        self.is_active = is_active
        self.frame = 0
        self.lives = lives
        self.animation = self.stay_l
        self.direction = DIRECTION_L
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x,y,self.rect.width,self.rect.height)

        self.is_knife = False
        self.is_dead = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.weapon = Hammer(self, 40)

        Fallable.create_ground_collition_rect(self)
        self.health_bar_width = 400
        self.health_bar_height = 20
        self.particle_list = ParticleList(self)

    def load_animations(self):
        p_scale = 0.6
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/bosses/troll_stone_hammer/WALK/WALK_00{0}.png",0,7,flip=True,scale=p_scale)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/bosses/troll_stone_hammer/IDLE/IDLE_00{0}.png",0,7,flip=True,scale=p_scale)
        self.knife_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/bosses/troll_stone_hammer/ATTAK/ATTAK_00{0}.png",0,7,flip=True,scale=p_scale)
        self.die = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/bosses/troll_stone_hammer/DIE/DIE_00{0}.png",0,6,scale=p_scale)
        self.hurt = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/bosses/troll_stone_hammer/HURT/HURT_00{0}.png",0,7,flip=True,scale=p_scale)
        # w = 491 
        # h = 417
        # lista = [self.stay_l, self.knife_l,self.hurt,self.die]
        # for animation in lista:
        #     for i in range(len(animation)):
        #         pygame.transform.scale(animation[i], (w,h))

    def do_animation(self,delta_ms):
        if self.is_dead and self.animation_ended():
            self.owner.kill_boss(self)
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
                    self.animation = self.stay_l

    def change_y(self,delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def receive_shoot(self, damage = 1) -> bool:
        self.animation = self.hurt
        self.lives -= damage 
        self.particle_list.create_hit_particle()
        if self.lives <= 0:
            self.is_dead = True            
            self.frame = 0
            self.animation = self.die

    def update(self,delta_ms,plataform_list, player_list):
        if self.is_active:
            if not self.died():
                self.do_movement(delta_ms, plataform_list)
                self.try_attack(player_list)
            
            self.do_animation(delta_ms) 

    def do_movement(self,delta_ms,plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        self.update_grounded(plataform_list)
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0

            self.update_gravity()

            self.change_y(self.velocity_y)

    def activate(self):
        self.is_active = True

    def draw(self,screen):
        if self.is_active:
            if(DEBUG):
                pygame.draw.rect(screen,color=(255,255 ,0),rect=self.collition_rect)
            self.image = self.animation[self.frame]
            screen.blit(self.image,self.rect)
            self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        # Calculate the width of the health bar based on the boss's current health

        health_percentage = (self.lives / self.max_health) * 100
        green_width = (health_percentage * self.health_bar_width) / 100

        # Calculate the position of the health bar relative to the boss's position
        health_bar_x = screen.get_width() // 2 - self.health_bar_width // 2
        health_bar_y = 50  # Adjust as needed

        # Draw the background of the health bar (red color)
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))

        # Draw the green portion of the health bar
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, green_width, self.health_bar_height))
    
    def try_attack(self, player_list):
        import random
        number = random.randint(1,100)
        if number <= 3:
            self.shoot()
        elif number <= 10:
            self.attack(player_list)
    
    def shoot(self):
        self.animation = self.knife_l
        if(self.can_shoot_again()):
            self.frame = 0
            self.is_shoot = True
            self.owner.boss_shoot(self.weapon.shoot())

    def attack(self, player_list):
        self.animation = self.knife_l
        for player in player_list:
            if CollisionHelper.player_colliding_with_entity(player, self) and not player.died():
                if not self.is_knife and self.can_shoot_again():
                    self.is_knife = True
                    player.receive_shoot(BOSS_DAMAGE)
                else:
                    self.is_knife = False