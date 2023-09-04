class Pixel:

    def __init__(self, red: int, green: int, blue: int):
        self.__red = red
        self.__green = green
        self.__blue = blue

    @classmethod
    def tuple_input(cls, tuple_rgb: tuple[int | str, int | str, int | str]):
        rgb = [0, 0, 0]
        for index, value in enumerate(tuple_rgb):
            match value:
                case int():
                    rgb[index] = value
                case str():
                    rgb[index] = int(value, 2)
        return cls(red=rgb[0], green=rgb[1], blue=rgb[2])

    def get_red(self) -> int:
        return self.__red

    def get_green(self) -> int:
        return self.__green

    def get_blue(self) -> int:
        return self.__blue

    def get_red_bin(self) -> str:
        return bin(self.__red).replace("0b", "").zfill(8)

    def get_green_bin(self) -> str:
        return bin(self.__green).replace("0b", "").zfill(8)

    def get_blue_bin(self) -> str:
        return bin(self.__blue).replace("0b", "").zfill(8)

    def get_rgb(self) -> tuple[int, int, int]:
        return self.get_red(), self.get_green(), self.get_blue()

    def get_rgb_bin(self) -> tuple[str, str, str]:
        return self.get_red_bin(), self.get_green_bin(), self.get_blue_bin()

    def set_red(self, value):
        match value:
            case int():
                self.__red = value
            case str():
                self.__red = int(value, 2)

    def set_green(self, value):
        match value:
            case int():
                self.__green = value
            case str():
                self.__green = int(value, 2)

    def set_blue(self, value):
        match value:
            case int():
                self.__blue = value
            case str():
                self.__blue = int(value, 2)

    def set_rgb(self, values):
        # assuming values is a tuple
        self.set_red(values[0])
        self.set_green(values[1])
        self.set_blue(values[2])

    def __str__(self) -> str:
        return f'RED={self.__red},GREEN={self.__green},BLUE={self.__blue}'

    def __repr__(self) -> str:
        return f'RGB({self.__red}, {self.__green}, {self.__blue})'
