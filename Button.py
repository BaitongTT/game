import pygame

class Button:
    def __init__(self, image_path, position):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = position)
    
    def draw(self, window):
        window.blit(self.image, self.rect)
        