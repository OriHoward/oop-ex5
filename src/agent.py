from Position import Position
from pokemon import Pokemon
from Drawable import Drawable


class Agent(Drawable):

    def __init__(self, _id, pos: tuple = None):
        self._id: int = _id
        self._value: int = 0
        self._src: int = _id
        self._dest: int = -1
        self._speed: float = 1
        self._load_factor: float = 0
        if pos is not None:
            # (*pos) unpacks the tuple
            # https://stackoverflow.com/questions/1993727/expanding-tuples-into-arguments/1993732
            self._pos = Position(*pos)
        else:
            self._pos = Position()
        self._icon_path: str = "../misc/agent.png"
        self._curr_pokemon: Pokemon = None
        self._placement: int = 0
        self._assigned_path = []

    def set_assigned_path(self, path: list):
        """
        Set current shortest path to the pokemon assigned to the agent.
        """
        self._assigned_path = path

    def get_assigned_path(self):
        """
        Return current assigned path to the pokemon.
        """
        return self._assigned_path

    def update_agent(self, value, src, dest, speed, pos):
        """
        Update agent attributes (used when parsing json).
        """
        self._value = value
        self._src = src
        self._dest = dest
        self._speed = speed
        self._pos = Position(*(pos.split(",")))

    def calculate_load_factor(self, dist: float) -> float:
        """
        Calculate load factor of the agent to a given distance (with regards to its current load factor).
        time = dist / speed
        """
        return self._load_factor + (dist / self._speed)

    def update_load_factor(self, dist: float) -> None:
        """
        Add to the load factor of the agent.
        """
        self._load_factor += dist / self._speed

    def get_pos(self):
        return self._pos

    def get_icon_path(self):
        return self._icon_path

    def get_icon_proportions(self):
        return 40, 40

    def set_curr_pokemon(self, pokemon: Pokemon):
        """
        Set pokemon agent is assigned to.
        """
        self._curr_pokemon = pokemon

    def get_pokemon(self):
        """
        Return pokemon agent is assigned to.
        """
        return self._curr_pokemon

    def set_placement(self, initial_spot: int):
        """
        Initial node ID where the agent is placed (the start node).
        Used for testing.
        """
        self._placement = initial_spot

    def get_placement(self):
        """
        Returns agent node placement.
        Used for testing.
        """
        return self._placement

    def get_speed(self):
        """
        Return speed of agent.
        """
        return self._speed

    def get_dest(self):
        """
        Destination is -1 if the agent reached its destination.
        """
        return self._dest

    def get_src(self):
        """
        Return current node ID of where the agent is placed.
        """
        return self._src

    def get_id(self):
        """
        Return agent ID number.
        """
        return self._id

    def __repr__(self):
        return f"Agent: {self._id}, {self._value}, {self._pos}, {self._src}"
