import numpy as np
from PIL import Image
from PIL.Image import Exif

from helper import EXIF_MAKE, ExifData, ResizeMode, Sizing, \
    STARTING_X, STARTING_Y, TEAM_MEMBERS, DESCRIPTION, Direction, SOFTWARE_TITLE


def get_pixels_from_image():
    """Function that will get pixels from pillow image object"""
    pass


def clear_least_significant_bits(bits):
    """Function that will clear the given amount of least significant bits"""
    pass


def shift_image_bits_asarray(image: Image.Image, direction: Direction, bit_amount: int) -> np.asarray:
    """
    Convert image to numpy array and perform bitwise operation
    :param image: Image object
    :param direction: Left bit shit or Right bit shift
    :param bit_amount: Amount of bits to shift
    :return: Image data as array
    """
    image_asarray = np.asarray(image)
    match direction:
        case Direction.LEFT:
            return np.left_shift(image_asarray, bit_amount)
        case Direction.RIGHT:
            return np.right_shift(image_asarray, bit_amount)


def embed_apl_exif(image_exif: Exif, data: tuple[int, int]) -> Exif:
    """
    Implement A Pixel Life metadata
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
    return f"A{width}P{height}L"


def resize_image(image: Image.Image, max_dimension: tuple[int, int], resize_mode=ResizeMode.DEFAULT) -> Image.Image:
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
    sizing_mode = Sizing.SMALLER
    if (current_image_height > max_height) and (current_image_width > max_width):
        sizing_mode = Sizing.BIGGER
    if (current_image_height > max_height) and (current_image_width < max_width):
        sizing_mode = Sizing.TALLER
    if (current_image_width > max_width) and (current_image_height < max_height):
        sizing_mode = Sizing.WIDER
    match resize_mode:
        case ResizeMode.DEFAULT:
            match sizing_mode:
                case Sizing.BIGGER:
                    image_copy = image_copy.crop((STARTING_X, STARTING_Y, max_width, max_height))
                case Sizing.TALLER:
                    image_copy.crop((STARTING_X, STARTING_Y, current_image_width, max_height))
                case Sizing.WIDER:
                    image_copy.crop((STARTING_X, STARTING_Y, max_width, current_image_height))
        case ResizeMode.SHRINK_TO_SCALE:
            match sizing_mode:
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


def set_least_significant_bits(bits, content):
    """Function that will set the given least significant bits to content"""
    pass
