import os

from dotenv import load_dotenv
import pygame
from pygame import Color, gfxdraw, display, time, font

from GameHandler import GameHandler

load_dotenv()


def main():
    screen = display.set_mode((int(os.getenv("WIDTH")), int(os.getenv("HEIGHT"))))
    screen.fill(Color(30, 30, 30))
    icon = pygame.image.load(r'../misc/icon.png')
    pygame.display.set_icon(icon)
    pygame.font.init()
    f = font.SysFont("Arial", 20, bold=True)
    pygame.display.set_caption("Happy This Is the Last Assignment")
    clock = time.Clock()
    game_handler = GameHandler()
    game_handler.init_connection()
    game_handler.parse_game_info()
    game_handler.get_graph().scale_positions()
    game_handler.start_game()
    client_os = game_handler.get_client()
    for curr_edge in game_handler.get_graph().get_parsed_edges():
        src = game_handler.get_graph().get_node(curr_edge.get_src())
        dest = game_handler.get_graph().get_node(curr_edge.get_dest())
        src_x, src_y = src.get_pos().get_scaled_x(), src.get_pos().get_scaled_y()
        dest_x, dest_y = dest.get_pos().get_scaled_x(), dest.get_pos().get_scaled_y()
        pygame.draw.line(screen, Color(255, 255, 255), (src_x, src_y), (dest_x, dest_y), width=2)
    for node in game_handler.get_graph().get_node_map().values():
        pos = node.get_pos()
        gfxdraw.filled_circle(screen, int(pos.get_scaled_x()), int(pos.get_scaled_y()), 15, Color(128, 216, 255))
        id_surface = f.render(str(node.get_key()), True, pygame.Color(222, 22, 22))
        id_rect = id_surface.get_rect(center=(pos.get_scaled_x(), pos.get_scaled_y()))
        screen.blit(id_surface, id_rect)

    while game_handler.is_running() == 'true':
        print(client_os.is_running())
        print(client_os.time_to_end())
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
