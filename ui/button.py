import pygame

class Button:
    def __init__(self, x, y, width, height, text ,callback ,color=(100,200,255),sound = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.font = pygame.font.SysFont(None, 24)
        self.sound = sound

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, (0,0,0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.sound :
                self.sound.play()
            self.callback()