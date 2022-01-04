from unittest import TestCase
from unittest.mock import MagicMock

import json

from GameHandler import GameHandler


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
        with open('TestData/test-pokemon-data.json') as test_f:
            test_case_data = json.load(test_f)
        pokemon_list = test_case_data.get("Pokemons")
        pokemon_list.append(json.loads(json.dumps(pokemon_list[0])))
        pokemon_list[1]["Pokemon"]["type"] = 1
        self.game_handler.client.get_pokemons = MagicMock(return_value=json.dumps(test_case_data))
        self.game_handler.update_pokemons()
        self.game_handler.update_pokemons()
        self.assertEqual(2, len(self.game_handler.parsed_pokemons.values()))

    def test_start_game(self):
        self.fail()

    def test_get_graph(self):
        self.fail()

    def test_is_running(self):
        self.assertTrue(self.game_handler.is_running())

    def test_calculate_fastest_path(self):
        self.fail()

    def test_get_edge_path(self):
        self.fail()

    def test_choose_next_edge(self):
        self.fail()
