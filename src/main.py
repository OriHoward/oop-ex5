import os

import pygame
from dotenv import load_dotenv
from pygame import display, constants

from GameHandler import GameHandler
from GameUI import GameUI

load_dotenv()


def main():
    screen = display.set_mode((int(os.getenv("WIDTH")), int(os.getenv("HEIGHT"))), flags=constants.RESIZABLE)
    game_handler = GameHandler()
    game_handler.init_connection()
    game_handler.parse_game_info()
    game_ui_handler = GameUI(screen)
    graphi = game_handler.get_graph()

    game_handler.start_game()
    client_os = game_handler.get_client()
    game_ui_handler.pygame_setup()
    game_info = ""

    try:
        while game_handler.is_running() == 'true':
            game_ui_handler.reset_color()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            game_handler.update_agents()
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

            for poke_to_draw in game_handler.parsed_pokemons.values():
                game_ui_handler.draw(poke_to_draw)

            for agent_to_draw in game_handler.agents.values():
                if agent_to_draw.curr_interval < agent_to_draw.refresh_interval:
                    agent_to_draw.curr_interval += agent_to_draw.refresh_interval / 10
                else:
                    client_os.move()
                    agent_to_draw.curr_interval = 0
                game_ui_handler.draw(agent_to_draw)

            game_handler.update_agents()
            game_ui_handler.scale_positions(game_handler.agents.values())
            game_handler.update_pokemons()
            game_info = game_ui_handler.show_game_info(client_os.get_info(), client_os.time_to_end())
            game_handler.find_path()
            game_handler.choose_next_edge()

            display.update()
            game_ui_handler.clock.tick(60)
    except:
        print("Game has ended")

    print(game_info)


if __name__ == '__main__':
    main()
