import os

from dotenv import load_dotenv
import pygame
from pygame import Color, gfxdraw, display, time, font

from pokemon import Pokemon
from Position import Position
from GameUI import GameUI
from GameHandler import GameHandler

load_dotenv()


def main():
    screen = display.set_mode((int(os.getenv("WIDTH")), int(os.getenv("HEIGHT"))))
    game_handler = GameHandler()
    game_handler.init_connection()
    game_handler.parse_game_info()
    game_ui_handler = GameUI(screen)
    graphi = game_handler.get_graph()

    game_ui_handler.create_proportion_mapping(graphi)
    game_ui_handler.scale_positions(graphi.get_node_map().values())
    game_ui_handler.scale_positions(game_handler.parsed_pokemons)
    game_ui_handler.scale_positions(game_handler.agents.values())

    game_handler.start_game()
    client_os = game_handler.get_client()
    game_ui_handler.pygame_setup()

    for curr_edge in graphi.get_parsed_edges():
        src = graphi.get_node(curr_edge.get_src())
        dest = graphi.get_node(curr_edge.get_dest())
        game_ui_handler.draw_lines(src, dest)

    for node in graphi.get_node_map().values():
        game_ui_handler.draw_circles(node.get_pos(), node.get_key())

    for poke in game_handler.parsed_pokemons:
        poke.draw(screen)

    for agent in game_handler.agents.values():
        agent.draw(screen)

    while game_handler.is_running() == 'true':
        print(client_os.is_running())
        print(client_os.time_to_end())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        display.update()
        game_ui_handler.clock.tick(60)

    # pokemons = client.get_pokemons()
    # agents = client.get_agents()
    # graph_json = client.get_graph()
    #
    # print(client.is_running())
    # print(client.time_to_end())
    #
    # # only after the agents were added the start function actually starts the game_ui_handler
    # client.add_agent("{\"id\":0}")
    #
    # client.start()


if __name__ == '__main__':
    main()

p1 = Pokemon(5, 1, "35.19381366747377, 32.102419275630254, 0.0")
p2 = Pokemon(5, 1, "35.19381366747377, 32.102419275630254, 0.0")
p3 = Pokemon(6, 1, "35.187594216303474,32.10378225882353,0.0")
print(p1 == p2)
s = set()
s.add(p1)
s.add(p2)
s.add(p3)
print(s)
