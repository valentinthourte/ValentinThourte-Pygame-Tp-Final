from file_helper import FileHelper
from platform_factory import PlatformFactory
import constantes  

class PlatformHelper():
    @staticmethod
    def get_platforms_l1():
        return FileHelper.get_platforms_from_csv_file("levels/platforms/l1.csv")

    @staticmethod
    def get_platforms_for_level(level: str):
        match level:
            case constantes.LEVEL_1:
                return PlatformHelper.get_platforms_l1()
            case _:
                return []