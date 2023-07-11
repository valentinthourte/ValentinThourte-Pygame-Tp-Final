import pygame

from timed_consumable import TimedConsumable

class DamageConsumable(TimedConsumable):
    def __init__(self, x, y, owner, damage_percent_increase) -> None:
        image_path = self.get_image_path()
        self.damage_increase = damage_percent_increase
        w = 32
        h = 32

        damage_increase_time = 15
        self.consumer = None
        super().__init__(x, y, image_path, w, h, owner, damage_increase_time)
    
    def get_image_path(self):
        return "images/assets/consumables/drink/damage.png"

    def effect(self, player):
        player.increase_damage(self.damage_increase)
        self.was_consumed = True
        self.consumer = player
        self.consume_time = pygame.time.get_ticks()
    


    