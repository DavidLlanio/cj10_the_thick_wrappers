from itertools import combinations

import numpy as np
from PIL import Image

from helper import decrypt, encrypt
from helper.constant import ResizeMode
from helper.utility import clear_least_significant_bits, image_resize


def verify_encryption(cover: Image.Image, secret: Image.Image) -> None:
    """Confirms that an image can be encrypted in a given cover image and decrypted"""
    if secret.size > cover.size:
        secret = image_resize(secret, cover.size, ResizeMode.SHRINK_TO_SCALE)
    encryption = encrypt.encrypt_image_to_image(cover, secret)
    decryption = decrypt.decrypt_image_from_image(encryption)
    # Clear bits of original image to simulate compression
    comparison = clear_least_significant_bits(np.array(secret), 4)
    decryption = np.array(decryption)
    height, width, _ = comparison.shape
    if secret.size < cover.size:
        decryption = decryption[:height, :width]

    assert np.all(comparison == decryption)


def test_image_encryption(all_images: list[str]) -> None:
    """Tests whether encryption-decryption works correctly for all image pairs."""
    for i1, i2 in combinations(all_images, r=2):
        print(i1, i2)
        cover = Image.open(i1)
        secret = Image.open(i2)
        verify_encryption(secret, secret)
        verify_encryption(cover, secret)
        verify_encryption(secret, cover)
