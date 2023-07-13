from file_helper import FileHelper
from platform_factory import PlatformFactory
import constantes  

class PlatformHelper():
    @staticmethod
    def get_platforms_l1():
        return FileHelper.get_platforms_from_json_file("levels/platforms/l1.json")

    @staticmethod
    def get_platforms_l2():
            return FileHelper.get_platforms_from_json_file("levels/platforms/l2.json")
    @staticmethod
    def get_platforms_l3():
            return FileHelper.get_platforms_from_json_file("levels/platforms/l3.json")


            
    @staticmethod
    def get_platforms_for_level(level: str):
        match level:
            case constantes.LEVEL_1:
                return PlatformHelper.get_platforms_l1()
            case constantes.LEVEL_2:
                return PlatformHelper.get_platforms_l2()
            case constantes.LEVEL_3:
                  return PlatformHelper.get_platforms_l3()
            case _:
                return []