import os
import pygame
from pygame import Surface, display, Color, font, time, gfxdraw

from DiGraph import DiGraph
from GraphNode import GraphNode
from GraphEdge import GraphEdge

pygame.font.init()

COLOR = Color(30, 30, 30)
FONT = font.SysFont("Arial", 20, bold=True)
CAPTION = "Happy This Is the Last Assignment"
ICON = r'../misc/icon.png'


class GameUI:

    def __init__(self, screen, screen_color=COLOR, f=FONT, caption: str = CAPTION, icon=ICON):
        self.screen = screen
        self.screen_color = screen_color
        self.screen.fill(screen_color)
        self.f = f
        self.caption = caption
        self.icon = icon
        self.clock = time.Clock()
        self.pygame_setup()
        self.proportions: dict = {}

    def pygame_setup(self):
        icon = pygame.image.load(self.icon)
        pygame.display.set_icon(icon)
        pygame.display.set_caption(self.caption)

    def draw_circles(self, pos, key=None, c_color=Color(128, 216, 255), t_color=Color(222, 22, 22)):
        gfxdraw.filled_circle(self.screen, int(pos.get_scaled_x()), int(pos.get_scaled_y()), 15, c_color)
        if key is not None:
            id_surface = self.f.render(str(key), True, t_color)
            id_rect = id_surface.get_rect(center=(pos.get_scaled_x(), pos.get_scaled_y()))
            self.screen.blit(id_surface, id_rect)

    def draw_lines(self, src, dest, l_color=Color(255, 255, 255)):
        src_x, src_y = src.get_pos().get_scaled_x(), src.get_pos().get_scaled_y()
        dest_x, dest_y = dest.get_pos().get_scaled_x(), dest.get_pos().get_scaled_y()
        pygame.draw.line(self.screen, l_color, (src_x, src_y), (dest_x, dest_y), width=2)

    def create_proportion_mapping(self, graph: DiGraph):
        graph_proportions = {}
        min_x = min_y = float("inf")
        max_x = max_y = float("-inf")
        for node in graph.get_node_map().values():
            node_pos = node.get_pos()
            node_x, node_y = node_pos.get_x(), node_pos.get_y()
            min_x = min(min_x, node_x)
            min_y = min(min_y, node_y)
            max_x = max(max_x, node_x)
            max_y = max(max_y, node_y)
        graph_proportions["x_proportions"] = (min_x, max_x)
        graph_proportions["y_proportions"] = (min_y, max_y)
        self.proportions = graph_proportions

    def draw(self, obj_to_draw):
        icon = pygame.image.load(obj_to_draw.icon_path)
        scaled_image = pygame.transform.scale(icon, (35, 35))
        rect = scaled_image.get_rect(center=(obj_to_draw._pos.get_scaled_x(), obj_to_draw._pos.get_scaled_y()))
        self.screen.blit(scaled_image, rect)

    def scale_positions(self, objects_to_scale):
        for node in objects_to_scale:
            node.get_pos().scale(self.proportions)

    def reset_color(self):
        self.screen.fill(self.screen_color)
# button class?
# draw nodes
# draw edges
