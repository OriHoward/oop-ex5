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
        self.game_handler.client.add_pokemons = MagicMock(return_value="{}")

    def test_update_agents(self):
        self.fail()

    def test_create_agents(self):
        self.fail()

    def test_parse_game_info(self):
        self.game_handler.parse_game_info()
        self.assertEqual(1, len(self.game_handler.parsed_pokemons.values()))
        self.assertEqual(2, len(self.game_handler.agents.values()))

    def test_add_pokemons(self):
        self.fail()

    def test_update_pokemons(self):
        self.fail()

    def test_init_connection(self):
        self.fail()

    def test_get_client(self):
        self.fail()

    def test_start_game(self):
        self.fail()

    def test_get_graph(self):
        self.fail()

    def test_is_running(self):
        self.fail()

    def test_calculate_fastest_path(self):
        self.fail()

    def test_get_edge_path(self):
        self.fail()

    def test_choose_next_edge(self):
        self.fail()
