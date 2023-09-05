from PIL import Image
import numpy as np

from helper.StegaImage import StegaImage


class Steganographizer:

    _stega_image: Image.Image = None

    def __init__(self, cover: Image, secret: Image):
        self._cover = StegaImage(cover)
        self._secret = StegaImage(secret)

    def encrypt_image(self) -> None:
        """
        Apply image steganography by resetting the cover image's least significant 4 bits,
        take the secret image's most significant 4 bits and add both values together
        """
        print("Encrypting Image...")
        self._cover.reset_lsb()
        self._secret.take_msb()
        stega_image_array = np.add(self._cover.get_image_array(), self._secret.get_image_array())
        self._stega_image = Image.fromarray(stega_image_array)
        print("Complete!")

    def save_image(self, destination: str) -> None:
        try:
            self._stega_image.save(destination)
        except AttributeError:
            print("No steganography image file found.")
