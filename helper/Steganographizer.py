from PIL import Image
import numpy as np

from helper.StegaImage import StegaImage


class Steganographizer:

    @staticmethod
    def encrypt_image(cover: Image.Image, secret: Image.Image) -> Image.Image:
        """
        Apply image steganography by resetting the cover image's least significant 4 bits,
        take the secret image's most significant 4 bits and add both numpy arrays together.
        Sum of arrays is converted back into Pillow Image and returned.
        """
        print("Encrypting Image...")
        s_cover = StegaImage(cover)
        s_secret = StegaImage(secret)
        s_cover.reset_lsb()
        s_secret.take_msb()
        stega_image_array = np.add(s_cover.get_image_array(), s_secret.get_image_array())
        print("Encryption Complete!")
        return Image.fromarray(stega_image_array)

    @staticmethod
    def decrypt_image(image: Image) -> Image:
        """
        Robin's implementation
        """
        pass
