class Weapon():
    def __init__(self, owner, damage = 1) -> None:
        self.default_damage = damage
        self.damage = damage
        self.owner = owner
    
    def shoot(self):
        pass

    def increase_damage(self, percent):
        self.damage = self.damage + self.damage * (percent / 100)
    
