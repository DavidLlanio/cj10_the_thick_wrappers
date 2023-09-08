import numpy as np
from PIL import Image
from PIL.Image import Exif

from helper import Direction, ExifData, EXIF_MAKE, TEAM_MEMBERS, SOFTWARE_TITLE, DESCRIPTION, ResizeMode, Sizing, \
    STARTING_X, STARTING_Y


def get_pixels_from_image(img) -> list:
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


def clear_least_significant_bits(bits):
    """Function that will clear the given amount of least significant bits"""
    pass


def shift_image_bits_asarray(image_array: np.ndarray, direction: Direction, bit_amount: int) -> np.asarray:
    """
    Convert image to numpy array and perform bitwise operation
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
    Implement In Plain Pixel metadata
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
    Build a secret code for decryption function to analyze
    :param size: Secret image dimensions
    :return: Encrypted message
    """
    width, height = size
    return f"I{width}P{height}P"


def image_resize(image: Image.Image, max_dimension: tuple[int, int], resize_mode=ResizeMode.DEFAULT) -> Image.Image:
    """
    Resize image object\n
    DEFAULT - Crop any exceeding dimensions\n
    SHRINK_TO_SCALE - Shrink image to scale of maximum dimensions while keeping aspect ratio\n
    :param image: Image object
    :param max_dimension: Dimensions image cannot exceed
    :param resize_mode: Resize mode
    :return: Resized Image object. Returns the same image if smaller than max dimensions
    """
    current_image_width, current_image_height = image.size
    max_width, max_height = max_dimension
    image_copy = image.copy()
    sizing_mode = image_size_compare(current_image_width, current_image_height, max_width, max_height)
    match resize_mode:
        case ResizeMode.DEFAULT:
            match sizing_mode:
                case Sizing.SMALLER:
                    pass
                case Sizing.BIGGER:
                    image_copy = image_copy.crop((STARTING_X, STARTING_Y, max_width, max_height))
                case Sizing.TALLER:
                    image_copy.crop((STARTING_X, STARTING_Y, current_image_width, max_height))
                case Sizing.WIDER:
                    image_copy.crop((STARTING_X, STARTING_Y, max_width, current_image_height))
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


def image_size_compare(image_width: int, image_height: int, max_width: int, max_height) -> Sizing:
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


def set_least_significant_bits(bits, content):
    """Function that will set the given least significant bits to content"""
    pass
