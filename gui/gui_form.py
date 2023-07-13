import pygame
from pygame.locals import *

class Form():
    forms_dict = {}
    last_active = None
    clean_forms_dict = {}
    selected_type = "L{0}_SP"
    def __init__(self,name,master_surface,x,y,w,h,color_background,color_border,active):
        self.forms_dict[name] = self
        self.clean_forms_dict[name] = self
        self.name = name
        self.master_surface = master_surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color_background = color_background
        self.color_border = color_border

        self.surface = pygame.Surface((w,h))
        self.slave_rect = self.surface.get_rect()
        self.slave_rect.x = x
        self.slave_rect.y = y
        self.active = active
        self.x = x
        self.y = y
        self.widget_list = []
        if(self.color_background != None):
            self.surface.fill(self.color_background)
    
    @staticmethod
    def restart_form(param):
        Form.forms_dict[param] = Form.clean_forms_dict[param]
        Form.forms_dict[param].restart()
        Form.set_active(param)

    @staticmethod
    def quit(param):
        import sys
        pygame.quit()
        sys.exit()
        
    @staticmethod
    def set_active(name):
        Form.last_active = Form.get_active()
        for aux_form in Form.forms_dict.values():
            aux_form.active = False
        Form.forms_dict[name].active = True

    @staticmethod
    def return_to_last_from(param):
        Form.set_active(Form.last_active.name)

    @staticmethod
    def get_active():
        for aux_form in Form.forms_dict.values():
            if(aux_form.active):
                return aux_form
        return None

    @staticmethod
    def remove(name):
        if name in Form.forms_dict:
            Form.forms_dict.pop(name)

    def render(self):
        pass

    def update(self,lista_eventos):
        for aux_widget in self.widget_list:
            aux_widget.update(lista_eventos)

    def draw(self):
        self.master_surface.blit(self.surface,self.slave_rect)
        for aux_widget in self.widget_list:    
            aux_widget.draw()