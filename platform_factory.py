import pygame
from plataforma import Plataform
# from constantes import *
import constantes

class PlatformFactory():

    @staticmethod
    def get_platforms_l1():
        plataform_list = []
        plataform_list.append(Plataform(x=400,y=500,width=50,height=50,type=0))
        plataform_list.append(Plataform(x=450,y=500,width=50,height=50,type=1))
        plataform_list.append(Plataform(x=500,y=500,width=50,height=50,type=2))   
        plataform_list.append(Plataform(x=600,y=430,width=50,height=50,type=12))
        plataform_list.append(Plataform(x=650,y=430,width=50,height=50,type=14))
        plataform_list.append(Plataform(x=750,y=360,width=50,height=50,type=12))
        plataform_list.append(Plataform(x=800,y=360,width=50,height=50,type=13))
        plataform_list.append(Plataform(x=850,y=360,width=50,height=50,type=13))
        plataform_list.append(Plataform(x=900,y=360,width=50,height=50,type=14))
        return plataform_list

    @staticmethod
    def get_platforms_for_level(level: str):
        match level:
            case constantes.LEVEL_1:
                return PlatformFactory.get_platforms_l1()
            case _:
                return []