from PIL import Image

from helper.stega_image import StegaImage


class Steganographizer:

    @staticmethod
    def encrypt_image(cover: Image.Image, secret: Image.Image) -> Image.Image:
        """
        Apply image steganography by resetting the cover image's least significant 4 bits,
        take the secret image's most significant 4 bits and add both numpy arrays together.
        Sum of arrays is converted back into Pillow Image and returned.
        :param cover: Image you want to hide into
        :param secret: Image you want to hide
        :return: A steganography Image object
        """
        s_cover = StegaImage(cover)
        s_secret = StegaImage(secret)
        s_cover.reset_lsb()
        s_secret.take_msb()
        s_stega = s_cover.get_image_array().copy()
        if len(s_secret.get_image_array()) < len(s_cover.get_image_array()):
            s_stega[:s_secret.get_image_array().shape[0], :s_secret.get_image_array().shape[1]] += s_secret.get_image_array()
        else:
            s_stega += s_secret.get_image_array()
        return Image.fromarray(s_stega)

    @staticmethod
    def decrypt_image(image: Image.Image) -> Image.Image:
        """
        Robin's implementation
        """
        pass
