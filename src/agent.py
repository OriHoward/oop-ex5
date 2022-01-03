from Position import Position


class Agent:

    def __init__(self, _id, pos: tuple = None):
        self._id: int = _id
        self.value: int = 0
        self.src: int = None
        self.dest: int = None
        self.speed: float = 1
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
        parsed_pos = tuple([float(coord) for coord in pos.split(",")])
        self._position = Position(*parsed_pos)
        print(f"agent updated {self._id}")
