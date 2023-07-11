from background import Background

class BackgroundManager():
    def __init__(self, screen_width, height,  path):
        bg = Background()
        self.width = screen_width
        self.height = height
        self.path = path
    
    