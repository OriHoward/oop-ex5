from Position import Position


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
            self._position = Position(*pos)
        else:
            self._position = Position()

    def update_agent(self, value, src, dest, speed, pos):
        self.value = value
        self.src = src
        self.dest = dest
        self.speed = speed
        self._position = Position(*(pos.split(",")))
        print(f"agent updated {self._id}")

    def calculate_load_factor(self, dist: float):
        return self.load_factor + (dist / self.speed)

    def update_load_factor(self, dist: float):
        self.load_factor += dist / self.speed
