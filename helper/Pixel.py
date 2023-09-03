class Pixel:
    def __init__(self, red, green, blue):
        self.__red = red
        self.__green = green
        self.__blue = blue

    def get_red(self):
        return self.__red

    def get_green(self):
        return self.__green

    def get_blue(self):
        return self.__blue

    def get_red_bin(self):
        return bin(self.__red).replace("0b", "").zfill(8)

    def get_green_bin(self):
        return bin(self.__green).replace("0b", "").zfill(8)

    def get_blue_bin(self):
        return bin(self.__blue).replace("0b", "").zfill(8)

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
