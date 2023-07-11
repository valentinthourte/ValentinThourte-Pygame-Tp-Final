import pygame
from constantes import *
from collision_helper import CollisionHelper

class Interactable():
    def __init__(self,x,y,w,h, image_path, owner, scale = True) -> None:
        self.image = pygame.image.load(image_path).convert_alpha()
        if scale:
            self.image = pygame.transform.scale(self.image, (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
    
        self.use_text = None
        self.use_text_rect = None
        self.was_used = False

    def update(self, player_list):
        for player in player_list:
            if CollisionHelper.player_colliding_with_entity(player, self):
                self.display_use()
            else:
                self.use_text = None 

    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, color=(255, 255, 0), rect=self.collition_rect)
        screen.blit(self.image, self.rect)
        if self.use_text:
            screen.blit(self.use_text, self.use_text_rect)

    def display_use(self):
        font = pygame.font.SysFont(None, 24)
        use_text = font.render("USE", True, (255, 255, 255))
        use_text_rect = use_text.get_rect()
        use_text_rect.center = (self.rect.centerx + 25, self.rect.y - 30)  

        self.use_text = use_text
        self.use_text_rect = use_text_rect
    
    def use(self, level, player):
        if not self.was_used:
            self.was_used = True
        