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

    def get_background2(self):
        return Color.get_compliment(self.__background)

    def get_color_rotation(self):
        return random.randint(20, 340)

    def get_link(self):
        return self.__link

class Color(Enum):
    RED = "#ffbe0b"
    ORANGE = "#fb5607"
    GREEN = "#ff006e"
    CYAN = "#8338ec"
    BLUE = "#3a86ff"

    @staticmethod
    def get_compliment(string):
        if string == Color.RED.value:
            return "#fd454d"

        if string == Color.ORANGE.value:
            return "#ebba71"

        if string == Color.GREEN.value:
            return "#b9b1ff"

        if string == Color.CYAN.value:
            return "#d5fff9"

        if string == Color.BLUE.value:
            return "#9ce99b"


