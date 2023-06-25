from abc import abstractmethod
class Animatable():
    def __init__(self):
        self.frame = 0
        self.animation = []
        
    def animation_ended(self):
        return self.frame >= len(self.animation) - 1

    @abstractmethod
    def do_animation(self, delta_ms):
        pass