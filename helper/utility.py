import re
from typing import Any, TypeVar

import numpy as np
from PIL import Image

T = TypeVar("T", int, np.signedinteger[Any])
NON_ASCII_PATTERN = re.compile("r[^\x00-\x7f]+")


def pixels_to_binary(img) -> list:
    """Translates an inputted image's pixels to binary"""
    pixels = img.load()
    width, height = img.size
    pixellist = []

    # Iterates through all of the picture's pixels, left to right then down
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            r, g, b = str(bin(r))[2:].zfill(8), str(bin(g))[2:].zfill(8), str(bin(b))[2:].zfill(8)
            pixellist.append((r, g, b))
    return pixellist
# print(TESTpixels_to_binary("/Users/maxencegilloteaux/Downloads/output(1).png"))

def clear_least_significant_bits(bits: T, n: int) -> T:
    """Replaces an intger's `n` least significant bits with zeroes

    param bits: An int, including an array of a NumPy int type
    param n: Number of bits to clear
    """
    bits >>= n
    return bits << n


def set_least_significant_bits(bits, content):
    """Function that will set the given least significant bits to content"""
    pass


def strip_non_ascii(text: str) -> str:
    """
    Removes non-ASCII characters from a string.

    param text: String to convert.
    """
    # https://stackoverflow.com/questions/2758921/regular-expression-that-finds-and-replaces-non-ascii-characters-with-python
    return text.encode().decode("ascii", "replace").replace("\ufffd", "")


def to_bytes(text: str) -> list[int]:
    """
    Converts a string to ASCII code.

    param text: String to convert.
    """
    return list(bytearray(text, "ascii"))
