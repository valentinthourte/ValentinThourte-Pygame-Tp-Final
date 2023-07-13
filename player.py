import pygame
from collision_helper import CollisionHelper
from constantes import *
from auxiliar import Auxiliar
from animatable import Animatable
from fallable import Fallable
from killable import Killable
from particle import ParticleList
from attacker import Attacker
from pistol import Pistol

class Player(Fallable, Attacker, Animatable, Killable):

    def __init__(self,id,x,y, name,speed_walk,speed_run,gravity,jump_power,frame_rate_ms,move_rate_ms,jump_height, owner, images_path, player_keys, p_scale=1,interval_time_jump=100, lives = 182) -> None:
        Fallable.__init__(self)
        Attacker.__init__(self, PLAYER_SHOOT_INTERVAL)
        Animatable.__init__(self)
        Killable.__init__(self, lives=lives)

        self.id = id
        self.name = name
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Idle ({0}).png",1,10,flip=False,scale=p_scale)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Idle ({0}).png",1,10,flip=True,scale=p_scale)
        self.jump_r = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Jump ({0}).png",1,10,flip=False,scale=p_scale)
        self.jump_l = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Jump ({0}).png",1,10,flip=True,scale=p_scale)
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Run ({0}).png",1,8,flip=False,scale=p_scale)
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Run ({0}).png",1,8,flip=True,scale=p_scale)
        self.shoot_r = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Shoot ({0}).png",1,3,flip=False,scale=p_scale,repeat_frame=2)
        self.shoot_l = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Shoot ({0}).png",1,3,flip=True,scale=p_scale,repeat_frame=2)
        self.knife_r = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Melee ({0}).png",1,7,flip=False,scale=p_scale,repeat_frame=1)
        self.knife_l = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Melee ({0}).png",1,7,flip=True,scale=p_scale,repeat_frame=1)
        self.die = Auxiliar.getSurfaceFromSeparateFiles(images_path + "/Dead ({0}).png",1,10,flip=False,scale=p_scale,repeat_frame=1)

        self.particle_list = ParticleList(self)
        self.starting_x = x
        self.starting_y = y
        self.frame = 0
        self.score = 0
        self.move_x = 0

        self.weapon = Pistol(self,45)
        self.score = 0
        
        self.velocity_y = 0
        self.acceleration_y = 0

        self.speed_walk = speed_walk
        self.speed_run = speed_run
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
        self.can_jump = True
        self.is_shoot = False
        self.is_knife = False
        self.is_dead = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height
        self.player_color = self.generate_player_color()

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0 # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump

        self.recieved_shot = True

        self.owner = owner
        self.player_keys = player_keys

    def set_name(self, name):
        self.name = name
        
    def generate_player_color(self):
        import random
        r = random.randint(50, 200)
        g = random.randint(50, 200)
        b = random.randint(50, 200)
        return (r,g,b)

    def reset_coords(self):
        self.set_x(self.starting_x)
        # self.set_y(self.starting_y)
    
    def reset(self):
        self.reset_coords()
        self.reset_health()
        self.reset_damage()
    def get_health(self):
        return self.lives
    
    def increase_damage(self, percent):
        self.weapon.increase_damage(percent)

    def reset_damage(self):
        self.weapon.reset_damage()

    def increase_score(self, score):
        self.score += score
    
    def get_name(self):
        return self.name

    def get_score(self):
        return self.score

    def walk(self,direction):
        if(self.direction != direction or (self.animation != self.walk_r and self.animation != self.walk_l)):
            self.frame = 0
            self.direction = direction
            if(direction == DIRECTION_R):
                if not CollisionHelper.is_against_right_edge(self):
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
            else:
                
                if not CollisionHelper.is_against_left_edge(self):
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l

    def shoot(self,on_off = True):
        self.is_shoot = on_off
        if(on_off == True and self.is_grounded):
            if(self.can_shoot_again()):
                self.frame = 0
                self.is_shoot = True
                if(self.direction == DIRECTION_R):
                    self.animation = self.shoot_r
                else:
                    self.animation = self.shoot_l
                self.owner.player_shoot(self.weapon.shoot(self.direction))
                

    def receive_shoot(self, damage = 1):
        self.lives -= damage
        self.particle_list.create_hit_particle()
        if self.died():
            self.on_death()

    def knife(self,on_off = True):
        self.is_knife = on_off
        if(on_off == True and self.is_grounded):
            if self.can_shoot_again():
                if(self.animation != self.knife_r and self.animation != self.knife_l):
                    self.frame = 0
                    if(self.direction == DIRECTION_R):
                        self.animation = self.knife_r
                    else:
                        self.animation = self.knife_l      
                    colliding_enemies = self.owner.get_colliding_enemies(self)
                    if (len(colliding_enemies) > 0):
                        for enemy in colliding_enemies:
                            if not enemy.died():
                                enemy.receive_shoot()     

    def jump(self):
        if(self.can_jump):
            self.jumped = True
            self.velocity_y = -self.jump_power
            if(self.direction == DIRECTION_R):
                self.animation = self.jump_r
            else:
                self.animation = self.jump_l
            self.frame = 0
            self.can_jump = False
        else:
            self.stay()

    def stay(self, change_animation = True):
        if(self.is_knife or self.is_shoot):
            return

        if change_animation:
            if(self.animation != self.stay_r and self.animation != self.stay_l):
                if(self.direction == DIRECTION_R):
                    self.animation = self.stay_r
                else:
                    self.animation = self.stay_l
        self.jumped = False
        self.move_x = 0
        self.move_y = 0
        self.frame = 0

    def change_x(self, delta_x):
        new_x = self.rect.x + delta_x
        if 0 <= new_x <= ANCHO_VENTANA - self.rect.width:
            self.rect.x += delta_x
            self.collition_rect.x += delta_x
            self.ground_collition_rect.x += delta_x

    def change_y(self, delta_y):
        new_y = self.rect.y + delta_y
        if 0 <= new_y <= ALTO_VENTANA - self.rect.height:
            self.rect.y += delta_y
            self.collition_rect.y += delta_y
            self.ground_collition_rect.y += delta_y
    
    def set_x(self,value):
        self.rect.x = value
        self.collition_rect.x = value
        self.ground_collition_rect.x = value


    def set_y(self, value):
        self.rect.y = value
        self.collition_rect.y = value
        self.ground_collition_rect.y = value

    def do_movement(self,delta_ms,plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        self.update_grounded(plataform_list)
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0
            super().update_gravity()
            self.update_x_velocity()

            self.change_x(self.move_x)
            self.change_y(self.velocity_y)        
    
    def picked_up(self, consumable):
        consumable.effect(self)

    def heal(self, amount):
        can_heal = self.lives < self.max_health
        if can_heal:
            self.lives += amount
        return can_heal

    def increase_damage(self, percent):
        self.weapon.increase_damage(percent)

    def update_x_velocity(self):
        if self.is_knife or self.is_shoot:
            self.move_x = 0

    def update_grounded(self, platform_list):
        super().update_grounded(platform_list)
        self.can_jump = self.is_grounded

    def do_animation(self,delta_ms):
        if self.is_dead and self.animation_ended():
            pass
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
    
    def update(self,delta_ms,plataform_list):
        self.do_animation(delta_ms)
        self.do_movement(delta_ms,plataform_list)
    
    def draw(self,screen):
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,255),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
        Fallable.draw(self, screen)
        self.image = self.animation[self.frame]
        screen.blit(self.image,self.rect)
        self.particle_list.show_particles(screen)
        self.draw_icon(screen)
        

    def draw_icon(self, screen):
        image = pygame.image.load(PLAYER_ICON_PATH).convert_alpha()
        image_width = image.get_width()
        image_height = image.get_height()

        icon_x = self.rect.left + self.rect.width // 2
        icon_y = self.rect.top
        image_x = icon_x - image_width // 2
        image_y = (icon_y - image_height)

        Auxiliar.transform_image_color(image, C_RED, self.player_color)
        
        # Draw the image
        screen.blit(image, (image_x, image_y))

        # Create the font object
        font = pygame.font.Font(None, 30)

        # Create the text surface
        text_surface = font.render(f"P{self.id}", True, self.player_color)

        # Get the dimensions of the text surface
        text_width, text_height = text_surface.get_size()

        # Calculate the position to center the text above the image
        text_x = icon_x - text_width // 2
        text_y = image_y - text_height - 10

        # Draw the text above the image
        screen.blit(text_surface, (text_x, text_y))

    def events(self,delta_ms,keys):
        self.tiempo_transcurrido += delta_ms
        if(keys[self.player_keys[LEFT]] and not keys[self.player_keys[RIGHT]]):
            self.walk(DIRECTION_L)

        if(not keys[self.player_keys[LEFT]] and keys[self.player_keys[RIGHT]]):
            self.walk(DIRECTION_R)

        if(not keys[self.player_keys[LEFT]] and not keys[self.player_keys[RIGHT]] and not keys[self.player_keys[JUMP]]):
            self.stay()
        if(keys[self.player_keys[LEFT]] and keys[self.player_keys[RIGHT]] and not keys[self.player_keys[JUMP]]):
            self.stay()  

        if(keys[self.player_keys[JUMP]]):
            if((self.tiempo_transcurrido - self.tiempo_last_jump) > self.interval_time_jump):
                self.jump()
                self.tiempo_last_jump = self.tiempo_transcurrido

        if(not keys[self.player_keys[SHOOT]]):
            self.shoot(False)  

        if(not keys[self.player_keys[ATTACK]]):
            self.knife(False)  

        if(keys[self.player_keys[SHOOT]] and not keys[self.player_keys[ATTACK]]):
            self.shoot()     
        
        if(keys[self.player_keys[ATTACK]] and not keys[self.player_keys[SHOOT]]):
            self.knife()   
        
        if (keys[self.player_keys[USE]]):
            self.use()

    def use(self):
        self.owner.check_use(self)

    def get_bullet_end_coords_from_direction(self, direction):
        coords = [0, self.rect.centery]
        if self.direction == DIRECTION_R:
            coords[0] = ANCHO_VENTANA
        return coords
    
    def on_death(self):
        self.is_dead = True
        self.frame = 0
        self.animation = self.die
        self.move_x = 0
        self.move_y = 0
    