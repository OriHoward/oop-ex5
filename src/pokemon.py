from Position import Position
import pygame


class Pokemon:

    def __init__(self, value: float = 0, _type: int = 0, pos: str = None):
        self._value: float = value
        self._type: int = _type
        self._pos: Position = Position(*(pos.split(',')))
        self.is_active = True
        self.is_assigned = False
        self.icon_path = "../misc/mew.png"

    def get_value(self):
        return self._value

    def get_type(self):
        return self._type

    def get_pos(self):
        if self._pos is None:
            raise Exception
        return self._pos

    def update_activity(self, new_status):
        self.is_active = new_status

    def update_assigned(self, new_status):
        self.is_assigned = new_status

    def draw(self, screen):
        icon = pygame.image.load(self.icon_path)
        scaled_image = pygame.transform.scale(icon, (35, 35))
        rect = scaled_image.get_rect(center=(self._pos.get_scaled_x(), self._pos.get_scaled_y()))
        screen.blit(scaled_image, rect)
