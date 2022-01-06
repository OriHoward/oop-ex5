import json

from pygame import time, gfxdraw, Surface

from ButtonUI import Button
from ConstantsUI import *
from DiGraph import DiGraph
from Drawable import Drawable


class GameUI:

    def __init__(self, screen: Surface, screen_color=BACKGROUND_COLOR, f=GAME_FONT, caption: str = SCREEN_CAPTION,
                 icon=SCREEN_ICON):
        self.screen = screen
        self.screen_color = screen_color
        self.game_font = f
        self.caption = caption
        self.icon = icon
        self.clock = time.Clock()
        self._pygame_setup()
        self.proportions: dict = {}
        self.game_buttons: list[Button] = []

    def _pygame_setup(self):
        """
        Setup for pygame window icon and title.
        These are constant and initialized in the constructor.
        """
        icon = pygame.image.load(self.icon)
        pygame.display.set_icon(icon)
        pygame.display.set_caption(self.caption)

    def draw_circles(self, pos, key=None, c_color=CIRCLE_COLOR, t_color=TEXT_COLOR):
        """
        Draw a filled circle on the surface with an option to display text on top of the circle.
        """
        gfxdraw.filled_circle(self.screen, int(pos.get_scaled_x()), int(pos.get_scaled_y()), 15, c_color)
        if key is not None:
            id_surface = self.game_font.render(str(key), True, t_color)
            id_rect = id_surface.get_rect(center=(pos.get_scaled_x(), pos.get_scaled_y()))
            self.screen.blit(id_surface, id_rect)

    def draw_lines(self, src, dest, l_color=LINE_COLOR):
        """
        Draw a line on the surface.
        """
        src_x, src_y = src.get_pos().get_scaled_x(), src.get_pos().get_scaled_y()
        dest_x, dest_y = dest.get_pos().get_scaled_x(), dest.get_pos().get_scaled_y()
        pygame.draw.line(self.screen, l_color, (src_x, src_y), (dest_x, dest_y), width=2)

    def create_proportion_mapping(self, graph: DiGraph):
        """
        Used when scaling the nodes.
        Find min and max values of node positions.
        """
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

    def draw_icon(self, obj_to_draw: Drawable):
        """
        Display Drawable object on screen.
        Drawable object have an icon and proportion.
        """
        icon = pygame.image.load(obj_to_draw.get_icon_path())
        scaled_image = pygame.transform.scale(icon, obj_to_draw.get_icon_proportions())
        rect = scaled_image.get_rect(
            center=(obj_to_draw.get_pos().get_scaled_x(), obj_to_draw.get_pos().get_scaled_y()))
        self.screen.blit(scaled_image, rect)

    def scale_positions(self, objects_to_scale):
        """
        Objects are scaled according to proportions.
        """
        for scalable_obj in objects_to_scale:
            scalable_obj.get_pos().scale(self.proportions, self.screen.get_width(), self.screen.get_height())

    def reset_color(self):
        """
        Reset main screen background.
        """
        self.screen.fill(self.screen_color)

    def show_game_info(self, game_info, time_to_end):
        """
        Display game info on screen.
        """
        info_as_dict = json.loads(game_info)
        info_as_dict = info_as_dict.get("GameServer")
        text_to_display = f"moves: {info_as_dict.get('moves')}," \
                          f" points: {info_as_dict.get('grade')}," \
                          f" game_level: {info_as_dict.get('game_level')}, time_to_end: {time_to_end}"
        id_surface = self.game_font.render(text_to_display, True, TEXT_COLOR)
        id_rect = id_surface.get_rect(
            center=(self.screen.get_width() - (id_surface.get_width()), self.screen.get_height() - 10))
        self.screen.blit(id_surface, id_rect)

    def add_button(self, button: Button):
        """
        Add game buttons to UI. Game buttons are objects from the Button class we implemented.
        """
        self.game_buttons.append(button)

    def display_buttons(self):
        """
        Display game buttons on screen.
        """
        for b in self.game_buttons:
            b.render(self.screen)

    def check_buttons_pressed(self):
        """
        Method to check if buttons were clicked.
        """
        for b in self.game_buttons:
            b.is_pressed()
