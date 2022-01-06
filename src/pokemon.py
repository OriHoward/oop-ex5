from math import fabs

from Drawable import Drawable
from GraphEdge import GraphEdge
from GraphNode import GraphNode
from Position import Position
import math


class Pokemon(Drawable):

    def __init__(self, value: float = 0, _type: int = 0, pos: str = None):
        self._value: float = value
        self._type: int = _type
        self._pos: Position = Position(*(pos.split(',')))
        self._is_active: bool = True
        self._is_assigned: bool = False
        self._edge: GraphEdge = None
        self._icon_path: str = "../misc/mew.png" if _type > 0 else "../misc/bullbasaur.png"
        self._ratio = 1

    def get_value(self):
        return self._value

    def get_type(self):
        return self._type

    def get_pos(self):
        if self._pos is None:
            raise Exception
        return self._pos

    def set_activity(self, new_status) -> None:
        self._is_active = new_status

    def set_assigned(self, new_status) -> None:
        self._is_assigned = new_status

    def set_edge(self, edge: GraphEdge):
        self._edge = edge

    def get_edge(self) -> GraphEdge:
        return self._edge

    def get_identifier(self) -> tuple[float, float, int]:
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
        return True if fabs(d1 + d2 - d3) <= math.pow(10, -5) else False

    def set_ratio(self, graph):
        src_node = graph.get_node(self.get_edge().get_src())
        dest_node = graph.get_node(self.get_edge().get_dest())
        src_to_poke = src_node.get_pos().distance(self.get_pos())
        src_to_dest = src_node.get_pos().distance(dest_node.get_pos())
        self._ratio = src_to_poke / src_to_dest

    def get_ratio(self):
        return self._ratio

    def get_icon_path(self):
        return self._icon_path

    def get_icon_proportions(self):
        mod = (self._value // 5) * 3  # floor division
        return 35 + mod, 35 + mod

    def get_assigned(self):
        return self._is_assigned

    def __repr__(self):
        return f"Pokemon: {self._value}, {self._edge}, {self._type}"
