from plataforma import MovingPlatform, Plataform
import constantes

class PlatformFactory():
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
    
    def get_left_moving_platform(x, y, width, height, distance, speed,direction):
        return MovingPlatform(x, y, width, height, constantes.LEFT_PLATFORM_TYPE, distance, speed,direction)
    
    def get_right_moving_platform(x, y, width, height, distance, speed,direction):
        return MovingPlatform(x, y, width, height, constantes.RIGHT_PLATFORM_TYPE, distance, speed,direction)
    
    def get_center_moving_platform(x, y, width, height, distance, speed,direction):
        return MovingPlatform(x, y, width, height, constantes.CENTER_PLATFORM_TYPE, distance, speed,direction)
    
    def get_moving_platform_from_platform(platform, distance, speed = 2, direction = constantes.DIRECTION_R):
        return MovingPlatform.from_parent(platform, distance, speed, starting_direction=direction)
    
    
    

    