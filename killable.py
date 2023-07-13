class Killable():
    def __init__(self, lives) -> None:
        self.lives = lives
        self.max_health = lives
        
    def died(self):
        return self.lives <= 0
    def reset_health(self):
        self.lives = self.max_health