import pygame
from plataforma import Plataform
# from constantes import *
import constantes

class PlatformFactory():

    @staticmethod
    def get_platforms_l1():

        
        plataform_list = PlatformFactory.get_wide_platform(400, 500, 25, 25, 1)
        plataform_list += PlatformFactory.get_wide_platform(600, 430, 25, 25, 0)
        plataform_list += PlatformFactory.get_wide_platform(750, 360, 25, 25, 2)
        

        return plataform_list

    @staticmethod
    def get_platforms_for_level(level: str):
        match level:
            case constantes.LEVEL_1:
                return PlatformFactory.get_platforms_l1()
            case _:
                return []
        
    @staticmethod
    def get_wide_platform(x, y, block_width, block_height, inner_block_amount):
        platform_list = []
        platform_list.append(PlatformFactory.get_left_platform(x, y, block_width, block_height))
        x += block_width
        for i in range(inner_block_amount):
            platform_list.append(PlatformFactory.get_center_platform(x, y, block_width, block_height))
            x += block_width
        platform_list.append(PlatformFactory.get_right_platform(x, y, block_width, block_height))
        return platform_list

    def get_left_platform(x, y, width, height):
        return Plataform(x, y, width, height, type=constantes.LEFT_PLATFORM_TYPE)
    
    def get_right_platform(x, y, width, height):
        return Plataform(x, y, width, height, type=constantes.RIGHT_PLATFORM_TYPE)
    
    def get_center_platform(x, y, width, height):
        return Plataform(x, y, width, height, type=constantes.CENTER_PLATFORM_TYPE)

    