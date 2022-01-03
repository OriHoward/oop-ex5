from Position import Position
import hashlib


class Pokemon:

    def __init__(self, value: float = 0, _type: int = 0, pos: str = None):
        self._value: float = value
        self._type: int = _type
        self._pos: Position = Position(*(pos.split(',')))
        self.is_active = True
        self.is_assigned = False

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
