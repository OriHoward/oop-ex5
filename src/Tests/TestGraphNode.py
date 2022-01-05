from unittest import TestCase

from DiGraph import DiGraph
from GraphEdge import GraphEdge


class TestGraphNode(TestCase):

    def setUp(self):
        self.graph = DiGraph()
        for n in range(4):
            self.graph.add_node(n)
        self.graph.add_edge(0, 1, 1)

    def test_get_src_map(self):
        self.assertEqual({}, self.graph.get_node(0).get_srcMap())

    def test_get_dest_map(self):
        curr_edge: GraphEdge = self.graph.get_node(0).get_destMap().get(1)

        self.assertEqual(curr_edge.get_dest(), 1)
        self.assertEqual(curr_edge.get_src(), 0)

    def test_get_key(self):
        self.assertEqual(self.graph.get_node(0).get_key(), 0)

    def test_set_dist(self):
        self.assertRaises(ValueError, self.graph.get_node(0).set_dist,"asd")