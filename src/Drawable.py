from abc import ABC, abstractmethod


class Drawable(ABC):

    @abstractmethod
    def get_icon_path(self):
        """
        Image file path.
        """
        pass

    @abstractmethod
    def get_icon_proportions(self):
        """
        Size of icon to display.
        """
        pass

    @abstractmethod
    def get_pos(self):
        """
        Position of object.
        """
        pass
