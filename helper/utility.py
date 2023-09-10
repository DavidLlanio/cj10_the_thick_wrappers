import re
from glob import glob
from os.path import join
from typing import Any, Optional, TypeVar

import numpy as np
from PIL import Image
from PIL.Image import Exif

from helper.constant import N_PLANES

from .constant import (
    DESCRIPTION, EXIF_MAKE, SOFTWARE_TITLE, STARTING_X, STARTING_Y,
    TEAM_MEMBERS, Direction, ExifData, ResizeMode, Sizing
)

T = TypeVar("T", int, np.signedinteger[Any])

EXIF_MODEL_PATTERN = re.compile(r"I(?P<width>\d*)P(?P<height>\d*)P")


def pixels_to_binary(img: Image.Image) -> list[tuple[str, str, str]]:
    """
    Translates an image's pixels to binary.

    :param img: A Pillow Image object.
    :return: A list of the tuples containing
    strings representing the bits of each pixel's
    red, green, and blue values.
    """
    pixels = img.load()
    width, height = img.size
    pixellist = []

    # Iterates through all of the picture's pixels, left to right then down
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:N_PLANES]
            r, g, b = (
                str(bin(r))[2:].zfill(8),
                str(bin(g))[2:].zfill(8),
                str(bin(b))[2:].zfill(8),
            )
            pixellist.append((r, g, b))
    return pixellist


def clear_least_significant_bits(bits: T, n: int) -> T:
    """
    Replaces an integer's `n` least significant bits with zeroes.

    :param bits: An int, including an array of a NumPy int type
    :param n: Number of bits to clear
    """
    bits >>= n
    return bits << n


def shift_image_bits_asarray(
    image_array: np.ndarray, direction: Direction, bit_amount: int
) -> np.array:
    """
    Converts image to numpy array and performs a left or right shift.

    :param image_array: Image numpy array value
    :param direction: Left bit shit or Right bit shift
    :param bit_amount: Amount of bits to shift
    :return: Image data as array
    """
    match direction:
        case Direction.LEFT:
            return np.left_shift(image_array, bit_amount)
        case Direction.RIGHT:
            return np.right_shift(image_array, bit_amount)


def exif_embed_ipp(image_exif: Exif, data: tuple[int, int]) -> Exif:
    """
    Embeds In Plain Pixel metadata in an image's Exif data.

    :param image_exif: Image metadata
    :param data: New metadata to embed
    :return: Updated image metadata
    """
    image_exif[ExifData.MAKE.value] = EXIF_MAKE
    image_exif[ExifData.MODEL.value] = exif_model_builder(data)
    image_exif[ExifData.ARTIST.value] = TEAM_MEMBERS
    image_exif[ExifData.SOFTWARE.value] = SOFTWARE_TITLE
    image_exif[ExifData.DESCRIPTION.value] = DESCRIPTION
    return image_exif


def exif_model_builder(size: tuple[int, int]) -> str:
    """
    Builds a secret code for decryption function to analyze.

    :param size: Secret image dimensions.
    :return: Encrypted message.
    """
    width, height = size
    return f"I{width}P{height}P"


def parse_exif(image_exif: Exif) -> Optional[tuple[int, int]]:
    """
    Recovers the original size of the hidden image embedded in Exif data.

    The data are converted to a (width, height) tuple, if possible, corresponding
    to the dimensions of a Pillow image.

    :param image_exif: Image metadata
    :return: a tuple containing the width and height of the original hidden image, or `None` if not possible
    """
    model_value: Optional[str] = image_exif.get(ExifData.MODEL.value)
    if model_value is None:
        return None

    match = EXIF_MODEL_PATTERN.search(model_value)
    if match is None:
        return None

    width = int(match.group("width"))
    height = int(match.group("height"))

    return (width, height)


def image_resize(
    image: Image.Image,
    max_dimension: tuple[int, int],
    resize_mode: ResizeMode = ResizeMode.DEFAULT,
) -> Image.Image:
    """
    Resizes an image object to fit a maximum dimension.

    Several modes are available:
    DEFAULT - Crop any exceeding dimensions
    SHRINK_TO_SCALE - Shrink image to scale of maximum dimensions while keeping aspect ratio

    :param image: Image object
    :param max_dimension: Dimensions image cannot exceed
    :param resize_mode: Resize mode
    :return: Resized Image object. Returns the same image if smaller than max dimensions
    """
    current_image_width, current_image_height = image.size
    max_width, max_height = max_dimension
    image_copy = image.copy()
    sizing_mode = image_size_compare(
        current_image_width, current_image_height, max_width, max_height
    )
    match resize_mode:
        case ResizeMode.DEFAULT:
            match sizing_mode:
                case Sizing.SMALLER:
                    pass
                case Sizing.BIGGER:
                    image_copy = image_copy.crop(
                        (STARTING_X, STARTING_Y, max_width, max_height)
                    )
                case Sizing.TALLER:
                    image_copy.crop(
                        (STARTING_X, STARTING_Y, current_image_width, max_height)
                    )
                case Sizing.WIDER:
                    image_copy.crop(
                        (STARTING_X, STARTING_Y, max_width, current_image_height)
                    )
        case ResizeMode.SHRINK_TO_SCALE:
            match sizing_mode:
                case Sizing.SMALLER:
                    pass
                case Sizing.BIGGER:
                    image_copy.thumbnail((max_width, max_height), Image.LANCZOS)
                case Sizing.TALLER:
                    height_ratio = current_image_height / max_height
                    new_width = int(current_image_width // height_ratio)
                    image_copy.thumbnail((new_width, max_height), Image.LANCZOS)
                case Sizing.WIDER:
                    width_ratio = current_image_width / max_width
                    new_height = int(current_image_height // width_ratio)
                    image_copy.thumbnail((max_width, new_height), Image.LANCZOS)
    return image_copy


def image_size_compare(
    image_width: int, image_height: int, max_width: int, max_height
) -> Sizing:
    """
    Determine whether image is smaller, bigger, taller or wider than maximum dimension

    :param image_width:
    :param image_height:
    :param max_width:
    :param max_height:
    :return: Sizing mode
    """
    if (image_width > max_width) and (image_height > max_height):
        return Sizing.BIGGER
    if (image_width < max_width) and (image_height > max_height):
        return Sizing.TALLER
    if (image_width > max_width) and (image_height < max_height):
        return Sizing.WIDER
    return Sizing.SMALLER


def strip_non_ascii(text: str) -> str:
    """
    Removes non-ASCII characters from a string.

    param text: String to convert.
    :return: The string minus any non-ASCII characters.
    """
    # https://stackoverflow.com/questions/2758921/regular-expression-that-finds-and-replaces-non-ascii-characters-with-python
    return text.encode().decode("ascii", "replace").replace("\ufffd", "")


def to_bytes(text: str) -> list[int]:
    """
    Converts a string to a list of its characters' ASCII codes.

    param text: String to convert.
    :return: List of ASCII codes corresponding to the string's characters.
    """
    return list(bytearray(text, "ascii"))


def list_images(dir: str) -> list[str]:
    """Lists all .png or .jpeg images in a directory

    param dir: Directory to list.
    :return: List of paths to images in directory.
    """
    return glob(join(dir, "*.png")) + glob(join(dir, "*.jp?g"))
