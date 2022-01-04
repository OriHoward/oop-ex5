from GraphNode import GraphNode
from Position import Position
import pygame
from sys import float_info
from math import fabs


class Pokemon:

    def __init__(self, value: float = 0, _type: int = 0, pos: str = None):
        self._value: float = value
        self._type: int = _type
        self._pos: Position = Position(*(pos.split(',')))
        self.is_active = True
        self.is_assigned = False
        self.icon_path = "../misc/mew.png" if _type > 0 else "../misc/dratini.png"

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



    def is_between(self, src: GraphNode, dest: GraphNode) -> bool:
        """
        True if Position p is on the edge.
        d1 + d2 = d3
        abs(d1 + d2 - d3) <= eps
        """
        d1 = src.get_pos().distance(self._pos)
        d2 = dest.get_pos().distance(self._pos)
        d3 = src.get_pos().distance(dest.get_pos())
        return True if fabs(d1 + d2 - d3) <= float_info.epsilon else False
