from enum import Enum
from typing import Any

import numpy as np
from numpy import ndarray, dtype

from Pixel import Pixel


class StegaImage:
    def __init__(self, image):
        self.image = image
        self.image_as_array = np.asarray(image)
        self.format = image.format
        self.size = image.size
        self.mode = image.mode

    def get_pixel_binary(self, coordinates: tuple[int, int]) -> ndarray[Any, dtype[Any]]:
        decimal_value = self.image_as_array[coordinates]
        px_bin = Pixel(decimal_value[0], decimal_value[1], decimal_value[2])
        return np.array(px_bin.get_rgb_bin())

    def get_pixel_lsb(self, coordinates) -> ndarray[Any, dtype[Any]]:
        px_bin = self.get_pixel_binary(coordinates)
        lsb_value = {}
        for index, binary in enumerate(px_bin):
            lsb = parse_sb(binary, SignificantBit.LSB)
            lsb_value[index] = lsb
        return np.array((lsb_value[0], lsb_value[1], lsb_value[2]))

    def get_pixel_msb(self, coordinates):
        px_bin = self.get_pixel_binary(coordinates)
        msb_value = []
        for index, binary in enumerate(px_bin):
            msb = parse_sb(binary, SignificantBit.MSB)
            msb_value.append(msb)
        return np.asarray(msb_value)

    def get_image_bits(self):
        height, width, mode = self.image_as_array.shape
        grid = np.empty(shape=(height, width), dtype='O')
        for y in range(height):
            for x in range(width):
                grid[y, x] = self.get_pixel_binary((y, x))
        return grid

    def get_image_lsb(self):
        height, width, mode = self.image_as_array.shape
        grid = np.empty(shape=(height, width), dtype='O')
        for y in range(height):
            for x in range(width):
                grid[y, x] = self.get_pixel_lsb((y, x))
        return grid

    def get_image_msb(self):
        height, width, mode = self.image_as_array.shape
        grid = np.empty(shape=(height, width), dtype='O')
        for y in range(height):
            for x in range(width):
                grid[y, x] = self.get_pixel_msb((y, x))
        return grid


class SignificantBit(Enum):
    MSB = 1
    LSB = 2


def parse_sb(binary: str, sb: SignificantBit) -> str:
    match sb:
        case SignificantBit.MSB:
            return binary[:4]
        case SignificantBit.LSB:
            return binary[4:]
