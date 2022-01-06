from Position import Position
from pokemon import Pokemon


class Agent:

    def __init__(self, _id, pos: tuple = None):
        self._id: int = _id
        self.value: int = 0
        self.src: int = None
        self.dest: int = None
        self.speed: float = 1
        self.load_factor: float = 0
        if pos is not None:
            # (*pos) unpacks the tuple
            # https://stackoverflow.com/questions/1993727/expanding-tuples-into-arguments/1993732
            self._pos = Position(*pos)
        else:
            self._pos = Position()
        self.icon_path: str = "../misc/pokeball.png"
        self.refresh_interval: float = 0
        self.curr_interval: float = 0
        self.curr_pokemon: Pokemon = None
        self.placement: int = 0

    def update_agent(self, value, src, dest, speed, pos):
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self._pos = Position(*(pos.split(",")))

    def calculate_load_factor(self, dist: float) -> float:
        return self.load_factor + (dist / self.speed)

    def update_load_factor(self, dist: float) -> float:
        self.load_factor += dist / self.speed

    def get_pos(self):
        return self._pos

    def set_refresh_interval(self, dist):
        self.refresh_interval = (dist / self.speed)

    def set_curr_pokemon(self, pokemon: Pokemon):
        self.curr_pokemon = pokemon

    def get_pokemon(self):
        return self.curr_pokemon

    def dist_from_poke(self) -> float:
        if self.curr_pokemon is not None:
            return self._pos.distance(self.curr_pokemon.get_pos())
        return float("inf")

    def set_placement(self, initial_spot):
        self.placement = initial_spot

    def get_speed(self):
        return self.speed

    def __repr__(self):
        return f"Agent: {self._id}, {self.value}, {self._pos}, {self.src}"
