from pygame import Rect, Surface

from ConstansUI import *


class Button:

    def __init__(self, title: str, button_font: font, size: tuple[int, int], position: tuple[int, int],
                 color: Color = BUTTON_COLOR, image_path: str = None):
        self.title = title
        self.button_font = button_font
        self.rect = Rect((0, 0), size)  # Rect((left, top), (width, height)) -> Rect
        self.color = color
        self.image_path = image_path
        self.listeners = []
        self.pos = position

    def add_listener(self, function):
        self.listeners.append(function)

    def render(self, surface: Surface):
        self.rect.topleft = self.pos
        title_surface = self.button_font.render(self.title, True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=self.rect.center)
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(title_surface, title_rect)

    def is_pressed(self):
        if len(self.listeners) > 0:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                clicked, _, _ = pygame.mouse.get_pressed()
                if clicked:
                    for function in self.listeners:
                        function()
