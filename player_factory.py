import pygame
from player import Player

class PlayerFactory():
    @staticmethod
    def get_player(id, x, y, owner, image_path, keys):
        return Player(id,x=x,y=y,speed_walk=50,speed_run=80,gravity=14,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140, owner=owner, images_path=image_path, player_keys=keys, p_scale=0.2,interval_time_jump=300)
        
