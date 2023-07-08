class Killable():
    def __init__(self, lives) -> None:
        self.lives = lives
        self.max_health = lives
        
    def died(self):
        return self.lives <= 0