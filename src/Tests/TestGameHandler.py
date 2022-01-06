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
        self.game_handler.client.is_running = MagicMock(return_value=True)
        self.game_handler.client.time_to_end = MagicMock(return_value=10)

    def test_update_agents(self):
        self.game_handler.parse_game_info()
        # this is freeing the second agent
        original_agent = self.test_agent_data.get("Agents")[1]
        original_agent_dest = original_agent.get("Agent").get("dest")
        self.test_agent_data.get("Agents")[1].get("Agent")['dest'] = 12
        self.game_handler.client.get_agents = MagicMock(return_value=json.dumps(self.test_agent_data))
        self.game_handler.update_agents()
        updated_agent = list(self.game_handler.agents.values())[1]
        self.assertNotEqual(original_agent_dest, updated_agent.get_dest())

    def test_create_agents(self):
        self.game_handler.parse_game_info()
        self.game_handler.create_agents(2)
        agent_list = list(self.game_handler.agents.values())
        first_agent, second_agent = agent_list
        self.assertEqual(9, first_agent.get_placement())
        self.assertEqual(10, second_agent.get_placement())

    def test_parse_game_info(self):
        self.game_handler.parse_game_info()
        self.assertEqual(2, len(self.game_handler.get_parsed_pokemons().values()))
        self.assertEqual(2, len(self.game_handler.get_agents().values()))

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
        first_agent, second_agent = self.game_handler.get_agents().values()
        self.assertEqual(actual_fastest_path, first_agent.get_assigned_path())
        self.assertEqual([], second_agent.get_assigned_path())
        pokemon_list = list(self.game_handler.parsed_pokemons.values())
        self.assertTrue(pokemon_list[0]._is_assigned)
        # this is freeing the second agent
        self.test_agent_data.get("Agents")[1]['dest'] = -1
        self.game_handler.find_path()
        first_agent, second_agent = self.game_handler.get_agents().values()
        self.assertEqual(actual_fastest_path, first_agent.get_assigned_path())
        self.assertEqual([], second_agent.get_assigned_path())
