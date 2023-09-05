from PIL import Image
import numpy as np


class Steganographizer:
    __stego_image = None

    def __init__(self, cover: Image, secret: Image):
        self.__cover = cover
        self.__secret = secret

    def encrypt_image(self) -> None:
        shift_amount = 4
        print("Encrypting Image...")
        cover_array = np.asarray(self.__cover)
        secret_array = np.asarray(self.__secret)
        cover_lsb_reset = (cover_array >> shift_amount) << shift_amount
        secret_msb_shift = secret_array >> shift_amount
        stega_bits = np.add(cover_lsb_reset, secret_msb_shift)
        self.__stego_image = Image.fromarray(stega_bits)
        print("Complete!")

    def save_image(self, destination: str) -> None:
        try:
            self.__stego_image.save(destination)
        except AttributeError:
            print("No steganography image file found.")
