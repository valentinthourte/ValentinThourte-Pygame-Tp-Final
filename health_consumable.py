import random
from consumable import Consumable
from constantes import *
import os


class HealthConsumable(Consumable):
    def __init__(self, x, y, owner, heal_amount) -> None:
        
        image_path = self.get_image_path()
        self.heal_amount = heal_amount
        w = 32
        h = 32
        super().__init__(x, y, image_path, w, h, owner, scale=False)

    def effect(self, player):
        if player.heal(self.heal_amount):
            super().effect(player)
    
    def get_image_path(self):
        images = os.listdir(FOOD_IMG_DIR)
        return f"{FOOD_IMG_DIR}/{random.randint(1, len(images))}.png"