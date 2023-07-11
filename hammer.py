

from bullet import Bullet
from weapon import Weapon


class Hammer(Weapon):
    def __init__(self, owner, damage=1) -> None:
        super().__init__(owner, damage)
    
    def shoot(self):
        import random
        y_variation = random.randint(self.owner.rect.top, self.owner.rect.bottom)
        return Bullet(self, self.owner.rect.x, y_variation,0,y_variation,10,"images/assets/rock.png",100,50,True,100,100,self.damage)