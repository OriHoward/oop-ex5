from pygame import Rect, Surface

from ConstantsUI import *


class Button:

    def __init__(self, title: str, button_font: font, size: tuple[int, int], position: tuple[int, int],
                 button_color: Color = BUTTON_COLOR, text_color=TEXT_COLOR, image_path: str = None):
        self.title = title
        self.button_font = button_font
        self.rect = Rect((0, 0), size)  # Rect((left, top), (width, height)) -> Rect
        self.button_color = button_color
        self.text_color = text_color
        self.image_path = image_path
        self.listeners = []
        self.pos = position

    def add_listener(self, function):
        self.listeners.append(function)

    def render(self, surface: Surface):
        self.rect.topleft = self.pos
        title_surface = self.button_font.render(self.title, True, self.text_color)
        title_rect = title_surface.get_rect(center=self.rect.center)
        pygame.draw.rect(surface, self.button_color, self.rect)
        surface.blit(title_surface, title_rect)

    def is_pressed(self):
        if len(self.listeners) > 0:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                clicked, _, _ = pygame.mouse.get_pressed()
                if clicked:
                    for function in self.listeners:
                        function()
