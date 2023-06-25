import pygame
import random
class Particle:
    def __init__(self, owner, x, y) -> None:
        self.owner = owner
        self.radius = random.randint(4,6)
        self.position_x = x
        self.position_y = y
        
        self.show_particle = False
        self.last_show_time = 0
        VELOCITY_VARIABILITY = 20
        self.velocity_x = (random.randint(0, VELOCITY_VARIABILITY) / 10) - VELOCITY_VARIABILITY / 20
        self.velocity_y = -2
        self.velocity = (self.velocity_x, self.velocity_y)

    def show(self, surface):
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y
        gravity = random.randint(0,3) / 10
        self.velocity_y += gravity
        self.radius -= 0.15
        if self.radius <= 0:
            self.owner.remove(self)
        else:
            pygame.draw.circle(surface, (230, 37, 72, 0.7), (self.position_x, self.position_y), self.radius)
    
class ParticleList:
    def __init__(self, owner) -> None:
        self.particle_list = []
        self.owner = owner
    
    def add(self, particle):
        self.particle_list.append(particle)

    def remove(self, particle):
        if particle in self.particle_list:
            self.particle_list.remove(particle)

    def show_particles(self, surface):
        for particle in self.particle_list:
            particle.show(surface)

    def create_hit_particle(self):
        for i in range(0, 20):
            PARTICLE_Y_VARIABILITY = 80
            PARTICLE_X_VARIABILITY = 40
            x = self.owner.rect.center[0] + (random.randint(0, PARTICLE_X_VARIABILITY) - PARTICLE_X_VARIABILITY / 2) 
            y = self.owner.rect.center[1] + (random.randint(0, PARTICLE_Y_VARIABILITY) - PARTICLE_Y_VARIABILITY / 2) 
            self.particle_list.append(Particle(self, x,y))