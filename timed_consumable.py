from consumable import Consumable
import pygame

class TimedConsumable(Consumable):
    def __init__(self, x, y,image_path,w,h, owner, effect_time) -> None:
        super().__init__(x, y, image_path, w, h, owner, scale=False)
        self.effect_time = effect_time
        self.was_consumed = False
        self.consume_time = 0

    def check_picked_up(self, player_list):
        if not self.was_consumed:
            return super().check_picked_up(player_list)
        
    def draw(self, screen):
        if not self.was_consumed:
            return super().draw(screen)
        
    def update(self, delta_ms, plataform_list):
        if not self.was_consumed:
            return super().update(delta_ms, plataform_list)
        else:
            time = pygame.time.get_ticks()
            if time - self.consume_time > self.effect_time * 1000:
                self.consumer.reset_damage()
                self.destroy()