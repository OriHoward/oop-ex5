import os

from dotenv import load_dotenv
import pygame
from pygame import display

from pokemon import Pokemon
from GameUI import GameUI
from GameHandler import GameHandler
import json

load_dotenv()


def main():
    screen = display.set_mode((int(os.getenv("WIDTH")), int(os.getenv("HEIGHT"))))
    game_handler = GameHandler()
    game_handler.init_connection()
    game_handler.parse_game_info()
    game_ui_handler = GameUI(screen)
    graphi = game_handler.get_graph()

    game_handler.start_game()
    client_os = game_handler.get_client()
    game_ui_handler.pygame_setup()

    while game_handler.is_running() == 'true':
        game_ui_handler.reset_color()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        game_ui_handler.create_proportion_mapping(graphi)
        game_ui_handler.scale_positions(graphi.get_node_map().values())
        game_ui_handler.scale_positions(game_handler.parsed_pokemons.values())
        game_ui_handler.scale_positions(game_handler.agents.values())

        for curr_edge in graphi.get_parsed_edges():
            src = graphi.get_node(curr_edge.get_src())
            dest = graphi.get_node(curr_edge.get_dest())
            game_ui_handler.draw_lines(src, dest)

        for node in graphi.get_node_map().values():
            game_ui_handler.draw_circles(node.get_pos(), node.get_key())

        game_handler.update_pokemons()
        game_handler.calculate_fastest_path()

        game_handler.choose_next_edge()

        for obj_to_draw in list(game_handler.agents.values()) + list(game_handler.parsed_pokemons.values()):
            game_ui_handler.draw(obj_to_draw)
        game_handler.update_agents()

        display.update()
        game_ui_handler.clock.tick(60)


if __name__ == '__main__':
    main()
