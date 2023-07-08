
from consumable import Consumable


class HealthConsumable(Consumable):
    def __init__(self, x, y, owner, heal_amount) -> None:
        image_path = "images/assets/caja.png"
        self.heal_amount = heal_amount
        w = 32
        h = 32
        super().__init__(x, y, image_path, w, h, owner)

    def effect(self, player):
        if player.heal(self.heal_amount):
            super().effect(player)