from unittest import TestCase

from DiGraph import DiGraph


class TestDiGraph(TestCase):

    def setUp(self) -> None:
        self.graph = DiGraph()
        for n in range(4):
            self.graph.add_node(n)
        self.graph.add_edge(0, 1, 1)
        self.graph.add_edge(0, 3, 7.7)
        self.graph.add_edge(1, 0, 1.1)

    def test_get_parsed_edges(self):
        edge_list = self.graph.get_parsed_edges()
        self.assertEqual(3, len(edge_list))
        self.assertEqual(0, edge_list[0].get_src())

    def test_get_node_map(self):
        node_map = self.graph.get_node_map()
        self.assertIsNotNone(node_map)
        self.assertEqual(len(node_map), 4)
        test_g = DiGraph()
        self.assertIsNotNone(test_g.get_node_map())

    def test_get_node(self):
        sample_node = self.graph.get_node(0)
        fake_node = self.graph.get_node(13)
        self.assertIsNone(fake_node)
        self.assertIsNotNone(sample_node)
        self.assertEqual(0, sample_node.get_key())

    def test_get_edge(self):
        real_edge = self.graph.get_edge(0, 1)
        fake_edge = self.graph.get_edge(0, 13)
        self.assertIsNotNone(real_edge)
        self.assertIsNone(fake_edge)

    def test_v_size(self):
        empty_graph = DiGraph()
        self.assertEqual(4, self.graph.v_size())
        self.assertEqual(0, empty_graph.v_size())

    def test_e_size(self):
        empty_graph = DiGraph()
        self.assertEqual(3, self.graph.e_size())
        self.assertEqual(0, empty_graph.e_size())

    def test_get_mc(self):
        empty_graph = DiGraph()
        self.assertEqual(7, self.graph.get_mc())
        self.assertEqual(0, empty_graph.get_mc())

    def test_add_edge(self):
        self.graph.add_edge(0, 3, 7)
        self.assertEqual(3, self.graph.e_size())

    def test_add_node(self):
        self.graph.add_node(5)
        self.assertEqual(5, self.graph.v_size())

    def test_get_all_v(self):
        node_map = self.graph.get_node_map()
        self.assertIsNotNone(node_map)
        self.assertEqual(len(node_map), 4)
        test_g = DiGraph()
        self.assertIsNotNone(test_g.get_node_map())

    def test_all_in_edges_of_node(self):
        expected_dict = {1: 1.1}
        result_dict = self.graph.all_in_edges_of_node(0)

        self.assertEqual(expected_dict, result_dict)

    def test_all_out_edges_of_node(self):
        expected_dict = {1: 1, 3: 7.7}
        result_dict = self.graph.all_out_edges_of_node(0)

        self.assertEqual(expected_dict, result_dict)
