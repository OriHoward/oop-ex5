from unittest import TestCase
from unittest.mock import MagicMock

import json

from GameHandler import GameHandler
from pokemon import Pokemon


class TestGameHandler(TestCase):

    def setUp(self) -> None:
        with open('TestData/test-game-info.json') as test_f:
            self.test_info_data = json.load(test_f)

        with open('TestData/test-pokemon-data.json') as test_f:
            self.test_pokemon_data = json.load(test_f)

        with open('TestData/test-agent-data.json') as test_f:
            self.test_agent_data = json.load(test_f)

        self.game_handler = GameHandler()
        self.game_handler.client.get_info = MagicMock(return_value=json.dumps(self.test_info_data))
        self.game_handler.client.get_pokemons = MagicMock(return_value=json.dumps(self.test_pokemon_data))
        self.game_handler.client.get_agents = MagicMock(return_value=json.dumps(self.test_agent_data))
        self.game_handler.client.add_agent = MagicMock(return_value="{}")
        self.game_handler.client.update_pokemons = MagicMock(return_value="{}")
        self.game_handler.client.is_running = MagicMock(return_value=True)

    def test_update_agents(self):
        self.fail()

    def test_create_agents(self):
        self.fail()

    def test_parse_game_info(self):
        self.game_handler.parse_game_info()
        self.assertEqual(1, len(self.game_handler.parsed_pokemons.values()))
        self.assertEqual(2, len(self.game_handler.agents.values()))

    def test_update_pokemons(self):
        self.game_handler.parse_game_info()
        with open('TestData/test-pokemon-data.json') as test_f:
            test_case_data = json.load(test_f)
        pokemon_list = test_case_data.get("Pokemons")
        pokemon_list.append(json.loads(json.dumps(pokemon_list[0])))
        pokemon_list[1]["Pokemon"]["type"] = 1
        self.game_handler.client.get_pokemons = MagicMock(return_value=json.dumps(test_case_data))
        self.game_handler.update_pokemons()
        parsed_pokemon: list[Pokemon] = list(self.game_handler.parsed_pokemons.values())
        first_poke, second_poke = parsed_pokemon
        self.assertEqual(10, first_poke.get_edge().get_src())
        self.assertEqual(9, second_poke.get_edge().get_src())
        self.assertEqual(2, len(self.game_handler.parsed_pokemons.values()))

    def test_get_graph(self):
        self.game_handler.parse_game_info()
        game_graph = self.game_handler.get_graph()
        self.assertEqual(22, game_graph.e_size())
        self.assertEqual(11, game_graph.v_size())

    def test_is_running(self):
        self.assertTrue(self.game_handler.is_running())

    def test_find_path(self):
        self.game_handler.parse_game_info()
        self.game_handler.find_path()
        actual_fastest_path = [0, 10, 9]
        first_agent_path, second_agent_path = self.game_handler.agents_map.values()
        self.assertEqual(actual_fastest_path, first_agent_path)
        self.assertEqual([], second_agent_path)
        pokemon_list = list(self.game_handler.parsed_pokemons.values())
        self.assertTrue(pokemon_list[0].is_assigned)
        # this is freeing the second agent
        self.test_agent_data.get("Agents")[1]['dest'] = -1
        self.game_handler.find_path()
        first_agent_path, second_agent_path = self.game_handler.agents_map.values()
        self.assertEqual(actual_fastest_path, first_agent_path)
        self.assertEqual([], second_agent_path)

    def test_get_edge_path(self):
        self.fail()

    def test_choose_next_edge(self):
        self.fail()
