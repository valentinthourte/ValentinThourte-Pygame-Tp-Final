class Killable():
    def __init__(self) -> None:
        self.lives = 1
    def died(self):
        return self.lives <= 0