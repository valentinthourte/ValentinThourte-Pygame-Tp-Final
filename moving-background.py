import pygame
from background import Background

class MovingBackground(Background): 
    def __init__(self, x, y,width, height,  path):
        
        bg_width = 2 * (width // 3)
        super().__init__(x, y,bg_width, height,  path)
