import numpy as np


class Stega:
    def __init__(self, image):
        self.__image = image
        self.format = image.format
        self.size = image.size
        self.mode = image.mode

    def get(self):
        return self.__image

    def get_pixel(self, coordinates):
        return self.__image.getpixel(coordinates)

    def get_pixel_binary(self, coordinates):
        # TODO: account for RGB, RGBA modes
        decimal_value = self.get_pixel(coordinates)
        binary_value = {}
        for index, dec in enumerate(decimal_value):
            binary_value[index] = bin(dec).replace("0b", "").zfill(8)
        return binary_value[0], binary_value[1], binary_value[2], binary_value[3]

    def get_pixel_lsb(self, coordinates):
        px_bin = self.get_pixel_binary(coordinates)
        lsb_value = {}
        for index, binary in enumerate(px_bin):
            lsb = parse_sb(binary)
            lsb_value[index] = lsb[1]
        return lsb_value[0], lsb_value[1], lsb_value[2], lsb_value[3]

    def get_pixel_msb(self, coordinates):
        px_bin = self.get_pixel_binary(coordinates)
        msb_value = {}
        for index, binary in enumerate(px_bin):
            msb = parse_sb(binary)
            msb_value[index] = msb[0]
        return msb_value[0], msb_value[1], msb_value[2], msb_value[3]

    def get_bits(self):
        grid = np.empty(shape=self.__image.size, dtype='O')
        width, height = self.__image.size
        for x in range(width):
            for y in range(height):
                grid[x, y] = self.get_pixel_binary((x, y))
        return grid

    def get_lsb(self):
        grid = np.empty(shape=self.__image.size, dtype='O')
        width, height = self.__image.size
        for x in range(width):
            for y in range(height):
                grid[x, y] = self.get_pixel_lsb((x, y))
        return grid

    def get_msb(self):
        grid = np.empty(shape=self.__image.size, dtype='O')
        width, height = self.__image.size
        for x in range(width):
            for y in range(height):
                grid[x, y] = self.get_pixel_msb((x, y))
        return grid


def parse_sb(binary):
    return binary[:4], binary[4:]
