import pygame

from interactable import Interactable


class ButtonInteractable(Interactable):
    def __init__(self, x, y, w, h, owner, scale=True) -> None:
        image_path = "images/assets/interactable/button.png"
        background = "images/assets/interactable/cabinet.png"
        self.bg_img = pygame.image.load(background).convert_alpha()
        
        super().__init__(x, y, w, h, image_path, owner, scale)
    
    def use(self, level, player):
        level.can_activate_boss = True
        super().use(level, player)
    
    def draw(self, screen):
        screen.blit(self.bg_img, (self.rect.x,self.rect.y))
        super().draw(screen)
