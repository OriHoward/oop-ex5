import os
import random

from math import dist


def random_num():
    """
    Generates a random number between [0, 100]
    """
    return random.randint(0, 100)


class Position:

    def __init__(self, x=None, y=None, z=None):
        """
        Generates a random number if there is a missing parameter in the constructor.
        """
        self._x = random_num() if x is None else float(x)
        self._y = random_num() if y is None else float(y)
        self._z = random_num() if z is None else float(z)
        self.scaled_x = 0
        self.scaled_y = 0

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_scaled_x(self):
        return self.scaled_x

    def get_scaled_y(self):
        return self.scaled_y

    def get_z(self):
        return self._z

    def get_as_tuple(self):
        return self._x, self._y

    def get_json_format_str(self):
        return f"{self._x},{self._y},{self._z}"

    def __str__(self):
        return "x={}, y={}, z={}".format(self._x, self._y, self._z)

    def scale(self, proportions: dict):
        screen_width = int(os.getenv("WIDTH")) - 50
        screen_height = int(os.getenv("HEIGHT")) - 50
        min_screen = 50
        x_proportions = proportions.get("x_proportions")
        y_proportions = proportions.get("y_proportions")
        min_x, max_x = x_proportions
        min_y, max_y = y_proportions

        self.scaled_x = ((self._x - min_x) / (max_x - min_x)) * (screen_width - min_screen) + min_screen
        self.scaled_y = ((self._y - min_y) / (max_y - min_y)) * (screen_height - min_screen) + min_screen

    def distance(self, p) -> float:
        """
        Calculate distance from this position to a given position.
        """
        return dist((self._x, self._y), (p.get_x(), p.get_y()))