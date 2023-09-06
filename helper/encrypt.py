from PIL import Image
from PIL.Image import Exif

from helper.utility import clear_least_significant_bits_asarray, msb_to_lsb_asarray


def encrypt_text_to_image():
    """Function that will encrypt text to image"""
    pass


def encrypt_image_to_image(cover: Image.Image, secret: Image.Image) -> Image.Image:
    """
    Apply image steganography by resetting the cover image's least significant 4 bits,
    take the secret image's most significant 4 bits and add both numpy arrays together.
    Sum of arrays is converted back into Pillow Image and returned.
    :param cover: Image you want to hide into
    :param secret: Image you want to hide
    :return: A steganography Image object
    """
    cover_msb = clear_least_significant_bits_asarray(cover)
    secret_msb = msb_to_lsb_asarray(secret)
    stega = cover_msb.copy()
    if secret_msb.size < cover_msb.size:
        height, width, _ = secret_msb.shape
        stega[:height, :width] += secret_msb
    else:
        stega += secret_msb
    return Image.fromarray(stega)
