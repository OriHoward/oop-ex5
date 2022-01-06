from unittest import TestCase
from unittest.mock import MagicMock

from GameHandler import GameHandler
import json
from pygame import display

from GameUI import GameUI
from pokemon import Pokemon


class TestGameUI(TestCase):
    def setUp(self) -> None:
        screen = display.set_mode((150, 150))
        with open('TestData/test-game-info.json') as test_f:
            self.test_info_data = json.load(test_f)

        with open('TestData/test-pokemon-data.json') as test_f:
            self.test_pokemon_data = json.load(test_f)

        with open('TestData/test-agent-data.json') as test_f:
            self.test_agent_data = json.load(test_f)
        self.game_handler = GameHandler()
        self.ui_handler = GameUI(screen, icon='../../misc/pokeball.png')
        self.game_handler.client.get_info = MagicMock(return_value=json.dumps(self.test_info_data))
        self.game_handler.client.get_pokemons = MagicMock(return_value=json.dumps(self.test_pokemon_data))
        self.game_handler.client.get_agents = MagicMock(return_value=json.dumps(self.test_agent_data))
        self.game_handler.client.add_agent = MagicMock(return_value="{}")
        self.game_handler.client.update_pokemons = MagicMock(return_value="{}")
        self.game_handler.client.is_running = MagicMock(return_value=True)

    def test_create_proportion_mapping(self):
        print("asdfl;kjasdf")
        self.game_handler.parse_game_info()
        self.ui_handler.create_proportion_mapping(self.game_handler.get_graph())
        proportions = self.ui_handler.proportions
        x_props = proportions["x_proportions"]
        y_props = proportions["y_proportions"]
        self.assertEqual(2, len(x_props))
        self.assertEqual(2, len(y_props))

    def test_scale_positions(self):
        self.game_handler.parse_game_info()
        self.ui_handler.create_proportion_mapping(self.game_handler.get_graph())
        pokemon_list: list[Pokemon] = list(self.game_handler.parsed_pokemons.values())
        self.ui_handler.scale_positions(pokemon_list)
        first_pokemon = pokemon_list[0]
        self.assertNotEqual(first_pokemon.get_pos().get_x(), first_pokemon.get_pos().get_scaled_x())
        self.assertNotEqual(first_pokemon.get_pos().get_scaled_y(), first_pokemon.get_pos().get_y())
