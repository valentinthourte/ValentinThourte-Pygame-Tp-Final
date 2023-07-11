from plataforma import Plataform
from constantes import *
from platform_factory import PlatformFactory

class FileHelper():
    @staticmethod
    def get_platform_from_csv_line(line):
        # line_split = FileHelper.clean_and_cast_platform_line(line)
        line_split = line.split(",")
        is_moving = line_split[-1] == "1"
        platform_x = line_split[0]
        platform_y = int(line_split[1])
        platform_width = int(line_split[2])
        if is_moving:
            x_split = platform_x.split("-")
            platform_x = int(x_split[0])
            distance = int(x_split[1]) - platform_x
        else:
            platform_x = int(platform_x)
        
        platform_list = PlatformFactory.get_wide_platform(platform_x, platform_y, PLATFORM_WIDTH, PLATFORM_HEIGHT, platform_width)
        if is_moving:
            direction = DIRECTION_R
            if distance < 0:
                direction = DIRECTION_L
            for index, platform in enumerate(platform_list):
                platform_list[index] = PlatformFactory.get_moving_platform_from_platform(platform, distance, direction=direction)
        return platform_list

    @staticmethod
    def get_platforms_from_csv_file(file):
        platform_list = []
        with open(file, "r") as csv:
            for line in csv:    
                platform_list += FileHelper.get_platform_from_csv_line(line.strip())
        return platform_list

    @staticmethod
    def clean_and_cast_platform_line(line):
        
        line_split = line.split(",")
        for i in range(len(line_split)):
            line_split[i] = int(line_split[i].strip())
        return line_split
        

