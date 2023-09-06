import string
from os.path import join
from random import choices

from PIL import Image

from helper import encrypt_text

chars = string.ascii_letters + string.digits + string.punctuation

images = ("cover_image.png", "output.png", "pydis_logo.png")


def pixel_count(image):
    """Get the nmber of pixels in an image"""
    return image.size[0] * image.size[1]


def decrypt_text(image: Image.Image) -> str | None:
    """Decrypt text encoded in an image

    If the message end is not found, `None`  is returned.
    """
    cols = image.size[0]
    end_length = len(encrypt_text.END_TEXT)
    # For last 3 bits
    modulus = 8
    decrypt = []
    endpoint = -end_length
    sequence = list(encrypt_text.END_TEXT)

    for pixel in (
        (
            n % cols,
            n // cols,
        )
        for n in range(image.size[0] * image.size[1])
    ):
        value = 0
        # Recover ASCII code
        for i, plane in enumerate(image.getpixel(pixel)):
            plane %= modulus
            # Shift bits back to original place - this ensures zero bits aren't lost
            # as leading zeroes
            plane <<= 3 * i
            value += plane
        decrypt.append(chr(value))
        # First character of message padding
        if decrypt[endpoint:] == sequence:
            return "".join(decrypt)[:endpoint]
    else:
        return None


def random_message(length: int) -> str:
    """
    Generate random characters of a certain length

    param length: Number of characters to select.
    """
    return "".join(choices(chars, k=length))


def encrypt_decrypt(message: str, image: Image.Image) -> None:
    """Confirm that a message can be encrypted in an image and recovered"""
    encryption = encrypt_text.encrypt_text(message, image)
    assert encryption
    decrypt = decrypt_text(encryption)
    assert message == decrypt


def too_long(image):
    """Should return `None` if message too long to encrypt"""
    extent = pixel_count(image)
    message = "a" * (extent + 1)
    result = encrypt_text.encrypt_text(message, image)
    assert result is None


end_length = len(encrypt_text.END_TEXT)


def test_messages():
    """Check encrypting-decrypting for messages of various lengths"""
    for file in images:
        image = Image.open(join("static", file))
        for length in (0, 1, 5, 10, 100, 1000, 5000, pixel_count(image) - end_length):
            too_long(image)
            message = random_message(length)
            encrypt_decrypt(message, image)
