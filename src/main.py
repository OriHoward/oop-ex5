import os

import pygame
from dotenv import load_dotenv
from pygame import display, constants, MOUSEBUTTONDOWN

from GameHandler import GameHandler
from GameUI import GameUI
from ButtonUI import Button
import math

load_dotenv()


def main():
    screen = display.set_mode((int(os.getenv("WIDTH")), int(os.getenv("HEIGHT"))), flags=constants.RESIZABLE)
    game_handler = GameHandler()
    game_handler.init_connection()
    game_handler.parse_game_info()
    game_ui_handler = GameUI(screen)
    graphi = game_handler.get_graph()

    client_os = game_handler.get_client()
    game_handler.start_game()

    game_ui_handler.pygame_setup()

    game_info = ""

    b = Button("Stop Game", game_ui_handler.game_font, (100, 30), (0, 0))
    b.add_listener(game_handler.get_client().stop_connection)
    game_ui_handler.add_button(b)
    move_queue = []
    move_counter = 0
    move_bound = math.ceil(float(client_os.time_to_end()) / 1000) * 10
    try:
        while game_handler.is_running() == 'true':
            game_ui_handler.reset_color()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == MOUSEBUTTONDOWN:
                    game_ui_handler.check_buttons_pressed()

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
                game_ui_handler.draw(agent_to_draw)

            if bool(move_queue) and float(client_os.time_to_end()) <= move_queue[0] and move_counter < move_bound:
                move_queue.pop(0)
                client_os.move()
                move_counter += 1
            elif not bool(move_queue) and move_counter < move_bound:
                client_os.move()
                move_counter += 1

            game_ui_handler.display_buttons()
            game_handler.update_agents()
            game_ui_handler.scale_positions(game_handler.agents.values())
            game_handler.update_pokemons()
            game_info = client_os.get_info()
            game_ui_handler.show_game_info(game_info, client_os.time_to_end())
            game_handler.find_path()
            game_handler.choose_next_edge(move_queue)
            move_queue = sorted(move_queue, reverse=True)

            display.update()
            game_ui_handler.clock.tick(60)
    except Exception as e:
        print(f"Game has ended {e}")

    print(game_info)


if __name__ == '__main__':
    main()
