from GraphNode import GraphNode
from GraphEdge import GraphEdge


class DiGraph:

    def __init__(self):
        self._nodeMap: dict[int, GraphNode] = {}
        self._MCount: int = 0
        self._parsed_edges: list[GraphEdge] = []

    def get_parsed_edges(self) -> list[GraphEdge]:
        """Returns a list of the edges in the graph"""
        return self._parsed_edges

    def get_node_map(self) -> dict[int, GraphNode]:
        """Returns a dictionary containing the nodes in the graph"""
        return self._nodeMap

    def get_node(self, key: int) -> GraphNode:
        """Returns a node in the graph. If it does not exist returns none"""
        return self._nodeMap.get(key)

    def get_edge(self, src: int, dest: int):
        """Returns an edge in the graph (if it exists)"""
        node = self._nodeMap.get(src, None)
        if node is None:
            return None
        return node.get_destMap().get(dest, None)

    def v_size(self) -> int:
        """Returns number of nodes in the graph"""
        return len(self._nodeMap)

    def e_size(self) -> int:
        """Returns the number of edges in the graph"""
        return len(self._parsed_edges)

    def get_mc(self) -> int:
        """Returns the number of changes made to the graph"""
        return self._MCount

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """Adds a valid edge to the graph. Overwrites if the edge exists"""
        src_node = self._nodeMap.get(id1)
        dest_node = self._nodeMap.get(id2)
        if src_node is None or dest_node is None or src_node == dest_node or weight < 0:
            return False
        edge = GraphEdge(id1, id2, weight)
        old_edge = src_node.get_destMap().get(id2)
        if old_edge is None:
            self._parsed_edges.append(edge)
        else:
            self._parsed_edges.remove(old_edge)
            self._parsed_edges.append(edge)
        src_node.add_dest(edge)
        dest_node.add_src(edge)
        self._MCount += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """Adds a node to the graph. Overwrites if the node exists"""
        try:
            self._nodeMap[node_id] = GraphNode(node_id, pos)
            self._MCount += 1
            return True
        except Exception as e:
            print(e)
            return False

    def initiate_edge_maps(self):
        """Initializes edge maps in DFS algorithm (after edges are transposed)"""
        for edge in self._parsed_edges:
            src_node = self._nodeMap.get(edge.get_src())
            dest_node = self._nodeMap.get(edge.get_dest())
            src_node.add_dest(edge)
            dest_node.add_src(edge)

    def get_all_v(self) -> dict:
        """Returns a dictionary of all the nodes in the graph.
            Each node is represented by a pair (node_id, node_object)
        """
        return self._nodeMap

    def all_in_edges_of_node(self, id1: int) -> dict:
        """Returns a dictionary of all the nodes that have edges into the given node.
        Each node is represented by a pair (other_node_id, weight)
         """
        if self.get_node(id1) is None or self.get_node(id1).get_srcMap() is None:
            return dict()
        edges = {key: value.get_weight() for (key, value) in self.get_node(id1).get_srcMap().items()}
        return edges

    def all_out_edges_of_node(self, id1: int) -> dict:
        """Returns a dictionary of all the nodes that have edges from the given node.
        Each node is represented by a pair (other_node_id, weight)
        """
        if self.get_node(id1) is None or self.get_node(id1).get_destMap() is None:
            return dict()
        edges = {key: value.get_weight() for (key, value) in self.get_node(id1).get_destMap().items()}
        return edges

    def __repr__(self):
        return f"Graph: |V|={self.v_size()}, |E|={self.e_size()}"
