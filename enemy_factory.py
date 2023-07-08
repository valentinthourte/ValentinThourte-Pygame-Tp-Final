import pygame

from enemigo import Enemy

class EnemyFactory():
    @staticmethod
    def get_ogre_enemy(x, y, owner):
        return Enemy(x=x,y=y,speed_walk=6,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140, owner=owner,p_scale=0.06,interval_time_jump=300)

