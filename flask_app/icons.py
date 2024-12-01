import random
from enum import Enum

class Icon:
    def __init__(self, text, background, link):
        self.__text = text
        self.__background = background
        self.__link = link

    def get_text(self):
        return self.__text

    def get_background(self):
        return self.__background

    def get_link(self):
        return self.__link

class Color(Enum):
    RED = "#ffbe0b"
    ORANGE = "#fb5607"
    GREEN = "#ff006e"
    CYAN = "#8338ec"
    BLUE = "#3a86ff"
