import pygame
from constantes import *

class Attacker():

    def __init__(self):
        self.last_shot_time = 0

    def can_shoot_again(self):
        actual_time = pygame.time.get_ticks()
        can_shoot = actual_time - self.last_shot_time > ENEMY_ATTACK_INTERVAL
        if can_shoot:
            self.last_shot_time = actual_time
        return can_shoot