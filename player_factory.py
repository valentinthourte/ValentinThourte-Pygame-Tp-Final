import pygame
from player import Player
from constantes import *

class PlayerFactory():
    @staticmethod
    def get_player(id, x, y, owner, image_path, keys, name = ""):
        return Player(id,x=x,y=y, name=name,speed_walk=15,speed_run=50,gravity=GRAVITY_SPEED,jump_power=40,frame_rate_ms=100,move_rate_ms=50,jump_height=140, owner=owner, images_path=image_path, player_keys=keys, p_scale=0.15,interval_time_jump=300)
        
