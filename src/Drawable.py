from abc import ABC, abstractmethod


class Drawable(ABC):

    @abstractmethod
    def get_icon_path(self):
        pass

    @abstractmethod
    def get_icon_proportions(self):
        pass

    @abstractmethod
    def get_pos(self):
        pass
