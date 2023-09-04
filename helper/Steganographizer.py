from PIL import Image
import numpy as np


class Steganographizer:

    stego_image = None

    def __init__(self, cover: Image, secret: Image):
        self.cover = cover
        self.secret = secret

    def encrypt_image(self) -> Image:
        cover_array = np.asarray(self.cover)
        secret_array = np.asarray(self.secret)
        cover_msb_shift = np.right_shift(4, cover_array)
        cover_lsb_reset = np.left_shift(4, cover_msb_shift)
        secret_msb_shift = np.right_shift(4, secret_array)
        stega_bits = np.add(cover_lsb_reset, secret_msb_shift)
        self.stego_image = Image.fromarray(stega_bits)

    def save_image(self, destination: str) -> None:
        self.stego_image.save(destination)
