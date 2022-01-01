import random


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

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def get_json_format_str(self):
        return f"{self._x},{self._y},{self._z}"

    def __str__(self):
        return "x={}, y={}, z={}".format(self._x, self._y, self._z)
