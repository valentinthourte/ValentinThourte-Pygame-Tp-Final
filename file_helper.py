from plataforma import Plataform
from constantes import *
from platform_factory import PlatformFactory
import json
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
                FileHelper.get_moving_platform_list_from_platform_list(platform_list=platform_list, distance=distance)

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
    
    @staticmethod
    def get_platforms_from_json_file(file):
        json_platforms = []
        with open(file, "r") as json_file:
            json_platforms = json.load(json_file)[JSON_PLATFORMS_KEY]

        platforms = []
        for platform in json_platforms:
            platforms += FileHelper.get_platform_object_from_json_object(platform)

        return platforms
    @staticmethod
    def get_platform_object_from_json_object(platform):
        start_x = platform[JSON_PLATFORM_X_KEY]
        start_y = platform[JSON_PLATFORM_Y_KEY]
        distance_x = platform[JSON_PLATFORM_DISTANCE_X_KEY]
        distance_y = platform[JSON_PLATFORM_DISTANCE_Y_KEY]
        inner_block_amount = platform[JSON_PLATFORM_INNER_AMOUNT_KEY]
        texture_type = platform[JSON_PLATFORM_TEXTURE_TYPE_KEY]
        speed = platform[JSON_PLATFORM_SPEED_KEY]

        platform_list = PlatformFactory.get_wide_platform(start_x, start_y, PLATFORM_WIDTH, PLATFORM_HEIGHT, inner_block_amount)
        
        if distance_x != 0 or distance_y != 0:
            FileHelper.get_moving_platform_list_from_platform_list(platform_list=platform_list, distance=distance_x, speed=speed)
        return platform_list
    
    @staticmethod
    def get_moving_platform_list_from_platform_list(platform_list, distance, speed):
        direction = DIRECTION_R
        if distance < 0:
            direction = DIRECTION_L
        for index, platform in enumerate(platform_list):
            platform_list[index] = PlatformFactory.get_moving_platform_from_platform(platform, distance,speed=speed, direction=direction)
        return platform_list

