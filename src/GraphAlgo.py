import copy
import json
from typing import List

from DiGraph import DiGraph
from GraphNode import GraphNode
import heapq


class GraphAlgo():

    def __init__(self, graph=None):
        if graph is None:
            self.graph: DiGraph = DiGraph()
        else:
            self.graph: DiGraph = graph

    def load_nodes(self, nodes) -> bool:
        """
        This function is responsible for loading the nodes array from the given JSON file.
        the counter it counting the amount of nodes that were parsed successfully
        """
        added_node_counter = 0
        if nodes is None:
            return False
        for node in nodes:
            node_id = node.get("id")
            pos: tuple = tuple(node.get("pos", "").split(',')[:-1])
            is_added = self.graph.add_node(node_id, pos)
            if is_added:
                added_node_counter += 1
        return True

    def load_edges(self, edges) -> bool:
        """
        This function is responsible for loading the edges array from the given JSON file.
        after the nodes are creates this function is then used to add the edges between the nodes.
        the counter it counting the amount of edges that were parsed successfully
        """
        added_edge_counter = 0
        if edges is None:
            return False
        for edge in edges:

            is_added = self.graph.add_edge(edge.get('src', None), edge.get('dest', None), edge.get('w', None))
            if is_added:
                added_edge_counter += 1
        return True

    def load_from_json(self, file_name: str) -> bool:
        """
        This function parses a given JSON file to a graph.
        it returns True if the function has successfully loaded the graph and False otherwise.
        """
        try:
            self.graph = DiGraph()
            with open(file_name, 'r') as f:
                json_dict = json.load(f)

            return self.load_nodes(json_dict["Nodes"]) and self.load_edges(json_dict["Edges"])

        except Exception as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        This function is calculating the distance between two given nodes in the graph using the dijkstra algorithm
        if there is no path is return (inf,[])
        """
        if id1 == id2 or self.graph.get_node_map().get(id1) is None or self.graph.get_node_map().get(id2) is None:
            return float('inf'), []
        prev = self.dijkstra(id1)
        prev.get(id2).append(id2)
        dest_node = self.graph.get_node(id2)
        if dest_node.get_dist() == float('inf'):
            return float('inf'), []
        return dest_node.get_dist(), prev.get(id2)

    def get_graph(self):
        return self.graph

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list.
        """
        if node_lst is None or len(node_lst) == 0:
            return list(), float('inf')
        if len(node_lst) == 1:
            return node_lst, 0
        cities = set(node_lst)  # set removes duplicates
        best_path, dist = self.get_optimal_path_to_cities(cities)
        self.remove_visited_cities(cities, best_path)
        path = list(best_path)
        while len(cities) > 0:
            path_from_end, dist_from_end = self.get_optimal_path(path[-1], cities, False)
            path_from_start, dist_from_start = self.get_optimal_path(path[0], cities, True)
            if path_from_start is None and path_from_end is None:
                return list(), float('inf')
            elif len(path_from_start) < len(path_from_end):
                path.extend(list(path_from_end))
                dist += dist_from_end
                self.remove_visited_cities(cities, path_from_end)
            else:
                path = list(path_from_start) + path
                dist += dist_from_start
                self.remove_visited_cities(cities, path_from_start)
        return path, dist

    @staticmethod
    def remove_visited_cities(cities: set[int], curr_path: tuple[int]):
        """
        Removes nodes from the set that are in the given path.
        """
        for key in curr_path:
            if key in cities:
                cities.remove(key)

    """
    lists are mutable which makes them unhashable so they can not be used as keys
    tuples are immutable so they can be used as keys
    further explanation: https://rollbar.com/blog/handling-unhashable-type-list-exceptions/
    """

    def get_optimal_path_to_cities(self, cities: set[int]):
        """
        Finds the shortest path between every pair of nodes.
        """
        path_map: dict[tuple[int], float] = dict()
        for key1 in cities:
            for key2 in cities:
                if key1 != key2:
                    dist, shortest_path = self.shortest_path(key1, key2)
                    if len(shortest_path) > 0 and shortest_path is not None:
                        path_map[tuple(shortest_path)] = dist
        return self.get_optimal_path_from_map(cities, path_map)

    @staticmethod
    def get_optimal_path_from_map(cities: set[int], path_map: dict[tuple[int], float]) -> (tuple[int], float):
        """
        Returns the path that minimizes the the distance of the path containing the maximum number of unique nodes.
        """
        max_size = 0
        best_path = tuple()
        for path in path_map.keys():
            curr_participants: set[int] = set()
            for city in cities:
                if city in path:
                    curr_participants.add(city)
            if len(curr_participants) > max_size:
                best_path = path
                max_size = len(curr_participants)
            elif (len(curr_participants) == max_size) and (best_path is not None) and \
                    (path_map.get(path) < path_map.get(best_path)):
                best_path = path
        return best_path, path_map.get(best_path)

    def get_optimal_path(self, node_id: int, cities: set[int], is_start: bool) -> (tuple[int], float):
        """
        Finds the shortest path from a given node to each node in the set. Returns the optimal path.
        the parameter (is_start) is to decide whether the given node is the start of the path or the end of it,
        this is used to check dijkstra
        (For optimal path: see function get_optimal_path_from_map documentation).
        """
        path_map: dict[tuple[int], float] = dict()
        for city in cities:
            if is_start:
                curr_dist, curr_shortest_path = self.shortest_path(city, node_id)
            else:
                curr_dist, curr_shortest_path = self.shortest_path(node_id, city)
            path_map[tuple(curr_shortest_path)] = curr_dist
        optimal_path, dist = self.get_optimal_path_from_map(cities, path_map)
        if optimal_path is None:
            return tuple(), -1
        else:
            path = list(optimal_path)
            if is_start:
                return tuple(path[:-1]), dist
            return tuple(path[1:]), dist

    def dijkstra(self, src: int) -> dict[int, list[int]]:
        """
        This version of the dijkstra algorithm also recreates the path from the src node to each node in the graph
        https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        """
        prev: dict[int, list[int]] = {}
        curr_node = self.graph.get_node(src)
        curr_node.set_dist(0.0)
        to_scan = []
        for node in self.graph.get_node_map().values():
            if node.get_key() != src:
                node.set_dist(float('inf'))
                prev[node.get_key()] = []
            heapq.heappush(to_scan, node)

        while len(to_scan) > 0:
            node: GraphNode = heapq.heappop(to_scan)
            for curr_edge in node.get_destMap().values():
                neighbor = self.graph.get_node(curr_edge.get_dest())
                alt = node.get_dist() + curr_edge.get_weight()
                if alt < neighbor.get_dist():
                    neighbor.set_dist(alt)
                    if prev.get(node.get_key(), None) is not None:
                        prev[neighbor.get_key()] = copy.deepcopy(prev.get(node.get_key()))
                    prev.get(neighbor.get_key(), []).append(node.get_key())
                    heapq.heappush(to_scan, neighbor)
        return prev

    def dijkstra_minimize(self, src: int):
        """
        This version of the dijkstra function is not copying objects that is why is it faster than the version above
        """
        curr_node = self.graph.get_node(src)
        curr_node.set_dist(0.0)
        to_scan = []
        for node in self.graph.get_node_map().values():
            if node.get_key() != src:
                node.set_dist(float('inf'))
            heapq.heappush(to_scan, node)
        while len(to_scan) > 0:
            node: GraphNode = heapq.heappop(to_scan)
            for curr_edge in node.get_destMap().values():
                neighbor = self.graph.get_node(curr_edge.get_dest())
                alt = node.get_dist() + curr_edge.get_weight()
                if alt < neighbor.get_dist():
                    neighbor.set_dist(alt)
                    heapq.heappush(to_scan, neighbor)

    def centerPoint(self) -> (int, float):
        """
        This function finds the center point in the graph using the dijkstra algorithm
        """
        if not self.is_connected():
            return None, float('inf')
        curr_minMax = float('inf')
        chosen_node = 0
        for curr_node_id in self.graph.get_node_map().keys():
            self.dijkstra_minimize(curr_node_id)
            minMax_index = self.find_max()
            node = self.graph.get_node(minMax_index)
            if node.get_dist() < curr_minMax:
                curr_minMax = node.get_dist()
                chosen_node = curr_node_id
        return chosen_node, curr_minMax

    def find_max(self) -> int:
        maximum = float('-inf')
        max_index = 0
        for curr_node in self.graph.get_node_map().values():
            if curr_node.get_dist() > maximum:
                maximum = curr_node.get_dist()
                max_index = curr_node.get_key()
        return max_index
