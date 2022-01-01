class GraphEdge:

    def __init__(self, src, dest, weight):
        self._src: int = int(src)
        self._dest: int = int(dest)
        self._weight: float = weight

    def get_src(self):
        """Returns ID of source node"""
        return self._src

    def get_dest(self):
        """Returns ID of destination node"""
        return self._dest

    def get_weight(self):
        """Returns edge weight"""
        return self._weight

    def set_dest(self, dest: int):
        """Sets the destination of the edge"""
        self._dest = dest

    def set_src(self, src: int):
        """Sets the source of the edge"""
        self._src = src

    def to_json_dict(self):
        return {
            "src": self._src,
            "w": self._weight,
            "dest": self._dest
        }
