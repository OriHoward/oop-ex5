import os

from dotenv import load_dotenv
import pygame
from pygame import Color, gfxdraw, display, time

from GameHandler import GameHandler

load_dotenv()


def main():
    screen = display.set_mode(
        (int(os.getenv("WIDTH")), int(os.getenv("HEIGHT")))
    )
    screen.fill(Color(0, 0, 0))
    clock = time.Clock()
    game_handler = GameHandler()
    game_handler.init_connection()
    game_handler.parse_game_info()
    game_handler.graph_algo.get_graph().scale_positions()
    game_handler.start_game()
    clientos = game_handler.get_client()
    for node in game_handler.graph_algo.get_graph().get_node_map().values():
        pos = node.get_pos()
        gfxdraw.filled_circle(screen, int(pos.get_x()), int(pos.get_y()), 15, Color(128, 216, 255))
    while game_handler.get_client().is_running() == 'true':
        print(clientos.is_running())
        print(clientos.time_to_end())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        display.update()
        clock.tick(60)

    # pokemons = client.get_pokemons()
    # agents = client.get_agents()
    # graph_json = client.get_graph()
    #
    # print(client.is_running())
    # print(client.time_to_end())
    #
    # # only after the agents were added the start function actually starts the game
    # client.add_agent("{\"id\":0}")
    #
    # client.start()


if __name__ == '__main__':
    main()
