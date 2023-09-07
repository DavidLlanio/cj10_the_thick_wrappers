from enum import Enum

from PIL import Image
import numpy as np
from PIL.Image import Exif

from helper.apl_info import APLInfo, APLExif


class ResizeMode(Enum):
    DEFAULT = 0
    SHRINK_TO_SCALE = 1


def get_pixels_from_image():
    """Function that will get pixels from pillow image object"""
    pass


def clear_least_significant_bits(bits):
    """Function that will clear the given amount of least significant bits"""
    pass


def clear_least_significant_bits_asarray(image: Image.Image) -> np.ndarray:
    bits = 4
    image_as_array = np.asarray(image)
    return (image_as_array >> bits) << bits


def msb_to_lsb_asarray(image: Image.Image) -> np.ndarray:
    bits = 4
    image_as_array = np.asarray(image)
    return image_as_array >> bits


def embed_exif(image_exif: Image.Image, data: APLInfo) -> Exif:
    exif = image_exif.getexif()
    exif[APLExif.MAKE.value] = data.make
    exif[APLExif.MODEL.value] = data.model
    exif[APLExif.ARTIST.value] = data.artist
    exif[APLExif.SOFTWARE.value] = data.software
    exif[APLExif.DESCRIPTION.value] = data.description
    return exif


def resize_image(image: Image.Image, max_dimension: tuple[int, int], mode=ResizeMode.DEFAULT) -> Image.Image:
    """
    Resize image object.\n
    DEFAULT - Crop any exceeding dimensions\n
    SHRINK_TO_SCALE - Shrink image to scale of maximum dimensions while keeping aspect ratio\n
    :param image: Image object
    :param max_dimension: Dimensions image cannot exceed
    :param mode: Resize mode
    :return: Resized Image object
    """
    current_image_width, current_image_height = image.size
    max_width, max_height = max_dimension
    image_copy = image.copy()
    match mode:
        case ResizeMode.DEFAULT:
            # if wider
            if (current_image_width > max_width) and (current_image_height < max_height):
                image_copy.crop((0, 0, max_width, current_image_height))
            # if taller
            if (current_image_height > max_height) and (current_image_width < max_width):
                image_copy.crop((0, 0, current_image_width, max_height))
            # if bigger
            if (current_image_height > max_height) and (current_image_width > max_width):
                image_copy = image_copy.crop((0, 0, max_width, max_height))
        case ResizeMode.SHRINK_TO_SCALE:
            # if wider
            if (current_image_width > max_width) and (current_image_height < max_height):
                width_ratio = current_image_width / max_width
                new_height = int(current_image_height // width_ratio)
                image_copy.thumbnail((max_width, new_height), Image.LANCZOS)
            # if taller
            if (current_image_height > max_height) and (current_image_width < max_width):
                height_ratio = current_image_height / max_height
                new_width = int(current_image_width // height_ratio)
                image_copy.thumbnail((new_width, max_height), Image.LANCZOS)
            # if bigger
            if (current_image_height > max_height) and (current_image_width > max_width):
                image_copy.thumbnail((max_width, max_height), Image.LANCZOS)
    return image_copy


def set_least_significant_bits(bits, content):
    """Function that will set the given least significant bits to content"""
    pass
