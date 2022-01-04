from math import fabs
from sys import float_info

from GraphEdge import GraphEdge
from GraphNode import GraphNode
from Position import Position


class Pokemon:

    def __init__(self, value: float = 0, _type: int = 0, pos: str = None):
        self._value: float = value
        self._type: int = _type
        self._pos: Position = Position(*(pos.split(',')))
        self.is_active = True
        self.is_assigned = False
        self.edge = None
        self.icon_path = "../misc/mew.png" if _type > 0 else "../misc/bullbasaur.png"

    def get_value(self):
        return self._value

    def get_type(self):
        return self._type

    def get_pos(self):
        if self._pos is None:
            raise Exception
        return self._pos

    def set_activity(self, new_status):
        self.is_active = new_status

    def set_assigned(self, new_status):
        self.is_assigned = new_status

    def set_edge(self, edge: GraphEdge):
        self.edge = edge

    def get_edge(self) -> GraphEdge:
        return self.edge

    def get_identifier(self):
        return self._pos.get_x(), self._pos.get_y(), self.get_type()

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

    def __repr__(self):
        return f"Pokemon: {self._value}, {self._pos}, {self._type}"
