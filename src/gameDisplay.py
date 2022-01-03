import os

from GameHandler import GameHandler
from pygame import gfxdraw
import pygame
from pygame import *

WIDTH, HEIGHT = 1080, 720

PORT = 6666
radius = 15
HOST = '127.0.0.1'
pygame.init()
screen = display.set_mode((int(os.getenv("WIDTH")), int(os.getenv("HEIGHT"))), flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)

handler = GameHandler()
handler.init_connection()
handler.parse_game_info()


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


min_x = min(handler.get_graph().get_node_map().values(), key=lambda node: node.get_pos().get_x()).get_pos().get_x()
max_x = max(handler.get_graph().get_node_map().values(), key=lambda node: node.get_pos().get_x()).get_pos().get_x()
min_y = min(handler.get_graph().get_node_map().values(), key=lambda node: node.get_pos().get_y()).get_pos().get_y()
max_y = max(handler.get_graph().get_node_map().values(), key=lambda node: node.get_pos().get_y()).get_pos().get_y()

handler.create_agents(1)
handler.start_game()

while handler.is_running() == 'true':
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    screen.fill(Color(0, 0, 0))

    for curr_node in handler.get_graph().get_node_map().values():
        pos_x = my_scale(curr_node.get_pos().get_x(), x=True)
        pos_y = my_scale(curr_node.get_pos().get_y(), y=True)
        pygame.gfxdraw.aacircle(screen, pos_x, pos_y, radius, pygame.Color(81, 45, 168))
        id_surface = FONT.render(str(curr_node.get_key()), True, Color(255, 255, 255))
        rect = id_surface.get_rect(center=(pos_x, pos_y))
        screen.blit(id_surface, rect)

    for curr_edge in handler.get_graph().get_parsed_edges():
        src = next(n for n in handler.get_graph().get_node_map().values() if n.get_key() == curr_edge.get_src())
        dest = next(n for n in handler.get_graph().get_node_map().values() if n.get_key() == curr_edge.get_dest())
        src_x = my_scale(src.get_pos().get_x(), x=True)
        src_y = my_scale(src.get_pos().get_y(), y=True)
        dest_x = my_scale(dest.get_pos().get_x(), x=True)
        dest_y = my_scale(dest.get_pos().get_y(), y=True)
        pygame.draw.line(screen, Color(72, 72, 72), (src_x, src_y), (dest_x, dest_y))
    pygame.display.update()
    clock.tick(60)
