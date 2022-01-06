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
    tmp_cntr = 0
    try:
        while game_handler.is_running() == 'true' and float(client_os.time_to_end()) > 3:
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
                # print(move_queue)
                move_queue.pop(0)
                client_os.move()
                move_counter += 1
            elif not bool(move_queue) and move_counter < move_bound:
                tmp_cntr += 1
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
    print(tmp_cntr, move_bound)


if __name__ == '__main__':
    main()

# WITH ELIF {"GameServer":{"pokemons":6,"is_logged_in":false,"moves":600,"grade":1644,"game_level":11,"max_user_level":-1,"id":0,"graph":"data/A2","agents":3}}
# WITHOUT ELIF {"GameServer":{"pokemons":6,"is_logged_in":false,"moves":600,"grade":1630,"game_level":11,"max_user_level":-1,"id":0,"graph":"data/A2","agents":3}}

# WITH ELIF {"GameServer":{"pokemons":4,"is_logged_in":false,"moves":242,"grade":480,"game_level":9,"max_user_level":-1,"id":0,"graph":"data/A2","agents":1}}
# WITH ELIF {"GameServer":{"pokemons":4,"is_logged_in":false,"moves":231,"grade":455,"game_level":9,"max_user_level":-1,"id":0,"graph":"data/A2","agents":1}}
# with elif and rounding mode half down {"GameServer":{"pokemons":4,"is_logged_in":false,"moves":248,"grade":487,"game_level":9,"max_user_level":-1,"id":0,"graph":"data/A2","agents":1}}
# with elif and rounding mode half up {"GameServer":{"pokemons":4,"is_logged_in":false,"moves":244,"grade":469,"game_level":9,"max_user_level":-1,"id":0,"graph":"data/A2","agents":1}}


# WITH ELIF {"GameServer":{"pokemons":5,"is_logged_in":false,"moves":117,"grade":333,"game_level":4,"max_user_level":-1,"id":0,"graph":"data/A1","agents":1}}
