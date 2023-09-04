from enum import Enum

import numpy as np

from helper.Pixel import Pixel


class StegaImage:
    def __init__(self, image):
        self.image = image
        self.image_as_array = np.asarray(image)
        self.format = image.format
        self.size = image.size
        self.mode = image.mode

    def get_pixel_binary(self, coordinates) -> tuple[str, str, str]:
        decimal_value = self.image_as_array[coordinates]
        px_bin = Pixel(decimal_value[0], decimal_value[1], decimal_value[2])
        return px_bin.get_rgb_bin()

    def get_pixel_lsb(self, coordinates) -> tuple[str, str, str]:
        px_bin = self.get_pixel_binary(coordinates)
        lsb_value = {}
        for index, binary in enumerate(px_bin):
            lsb = parse_sb(binary, SignificantBit.LSB)
            lsb_value[index] = lsb
        return lsb_value[0], lsb_value[1], lsb_value[2]

    def get_pixel_msb(self, coordinates) -> tuple[str, str, str]:
        px_bin = self.get_pixel_binary(coordinates)
        msb_value = {}
        for index, binary in enumerate(px_bin):
            msb = parse_sb(binary, SignificantBit.MSB)
            msb_value[index] = msb
        return msb_value[0], msb_value[1], msb_value[2]

    def get_image_bits(self):
        height, width, mode = self.image_as_array.shape
        grid = np.empty(shape=(width, height), dtype='O')
        for x in range(width):
            for y in range(height):
                grid[x, y] = self.get_pixel_binary((y, x))
        return grid

    def get_image_lsb(self):
        height, width, mode = self.image_as_array.shape
        grid = np.empty(shape=(width, height), dtype='O')
        for x in range(width):
            for y in range(height):
                grid[x, y] = self.get_pixel_lsb((y, x))
        return grid

    def get_image_msb(self):
        height, width, mode = self.image_as_array.shape
        grid = np.empty(shape=(width, height), dtype='O')
        for x in range(width):
            for y in range(height):
                grid[x, y] = self.get_pixel_msb((y, x))
        return grid

    def set_pixel_lsb(self, coordinates: tuple[int, int], lsb: tuple[str, str, str]):
        msb = self.get_pixel_msb(coordinates)
        new_bits = []
        for index, value in enumerate(msb):
            new_bits[index] = merge_sb(value, lsb[index])
        new_pixel = Pixel(int(new_bits[0]), int(new_bits[1]), int(new_bits[2]))
        self.image.putpixel(coordinates, new_pixel.get_rgb())


class SignificantBit(Enum):
    MSB = 1
    LSB = 2


def parse_sb(binary: str, sb: SignificantBit) -> str:
    match sb:
        case SignificantBit.MSB:
            return binary[:4]
        case SignificantBit.LSB:
            return binary[4:]


def merge_sb(msb: str, lsb: str) -> str:
    return msb + lsb
