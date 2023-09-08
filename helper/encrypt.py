import numpy as np
from PIL import Image

from helper import Direction, BITS_4, shift_image_bits_asarray


def encrypt_text_to_image():
    """Function that will encrypt text to image"""
    pass


def encrypt_image_to_image(cover: Image.Image, secret: Image.Image) -> Image.Image:
    """
    Apply image steganography by resetting the cover image's least significant 4 bits,
    take the secret image's most significant 4 bits and add both numpy arrays together\n
    Sum of arrays is converted back into Pillow Image and returned
    :param cover: Image you want to hide into
    :param secret: Image you want to hide
    :return: A steganography Image object
    """
    cover_asarray = np.asarray(cover)
    secret_asarray = np.asarray(secret)
    cover_msb = shift_image_bits_asarray(cover_asarray, Direction.RIGHT, BITS_4)
    cover_lsb_reset = shift_image_bits_asarray(cover_msb, Direction.LEFT, BITS_4)
    secret_msb = shift_image_bits_asarray(secret_asarray, Direction.RIGHT, BITS_4)
    stega_asarray = cover_lsb_reset.copy()
    if secret_msb.size < cover_lsb_reset.size:
        height, width, _ = secret_msb.shape
        stega_asarray[:height, :width] += secret_msb
    else:
        stega_asarray += secret_msb
    return Image.fromarray(stega_asarray)
