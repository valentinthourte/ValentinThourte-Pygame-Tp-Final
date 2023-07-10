import pygame
from constantes import *
from fallable import Fallable

class Victory(Fallable):
    def __init__(self,owner, image_path, width, height, x, y, final_font_size,frame_rate_ms = 100,move_rate_ms = 50) -> None:
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(width,height))

        self.final_font_size = final_font_size
        self.delta_font_size = self.final_font_size / EXPAND_TIME
        self.font_size = 0
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(self.rect)
        Fallable.__init__(self)
        self.last_draw_time = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.owner = owner
        Fallable.create_ground_collition_rect(self)

    def draw(self, screen):
        Fallable.draw(self, screen)
        screen.blit(self.image,self.rect)
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)

    def show_victory(self, screen):
        delta_draw_time = pygame.time.get_ticks() - self.last_draw_time
        print (delta_draw_time)
        if delta_draw_time > EXPAND_TIME / self.final_font_size and not self.font_size >= self.final_font_size: 
            self.last_draw_time = pygame.time.get_ticks()
            self.font_size += 1
        font = pygame.font.Font(None, self.font_size)
        text = font.render("Victory!", True, C_VICTORY) 
        text_rect = text.get_rect()
        text_rect.center = (ANCHO_VENTANA // 2, ALTO_VENTANA // 3)
        screen.blit(text, text_rect)
        return self.font_size >= self.final_font_size and delta_draw_time > 1000

    def update(self, delta_ms, plataform_list):
        self.tiempo_transcurrido_move += delta_ms
        self.update_grounded(plataform_list)
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0
            super().update_gravity()
            self.change_y(self.velocity_y)

    def change_y(self,delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y
    
