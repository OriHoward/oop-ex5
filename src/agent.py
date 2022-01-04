from Position import Position
import pygame


class Agent:

    def __init__(self, _id, pos: tuple = None):
        self._id: int = _id
        self.value: int = 0
        self.src: int = None
        self.dest: int = None
        self.speed: float = 1
        self.load_factor = 0
        if pos is not None:
            # (*pos) unpacks the tuple
            # https://stackoverflow.com/questions/1993727/expanding-tuples-into-arguments/1993732
            self._pos = Position(*pos)
        else:
            self._pos = Position()
        self.icon_path = "../misc/pokeball.png"
        self.refresh_interval = 0
        self.curr_interval = 0

    def update_agent(self, value, src, dest, speed, pos):
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self._pos = Position(*(pos.split(",")))

    def calculate_load_factor(self, dist: float):
        return self.load_factor + (dist / self.speed)

    def update_load_factor(self, dist: float):
        self.load_factor += dist / self.speed

    def get_pos(self):
        return self._pos

    def set_refresh_interval(self, dist):
        self.refresh_interval = (dist / self.speed) / 5

    def __repr__(self):
        return f"Agent: {self._id}, {self.value}, {self._pos}, {self.src}"
