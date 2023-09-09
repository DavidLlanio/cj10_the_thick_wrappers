import string
from glob import glob
from os.path import join
from random import choices

from PIL import Image

from helper import decrypt, encrypt, utility

ascii = string.ascii_letters + string.digits + string.punctuation
non_ascii = "".join(map(chr, range(128, 1000)))
combined = ascii + non_ascii
end_length = len(encrypt.END_TEXT)

img_dir = ".static"
images = glob(join(img_dir, "*.png"))


def pixel_count(image: Image.Image):
    """Get the number of pixels in an image"""
    return image.size[0] * image.size[1]


def decrypt_text(image: Image.Image) -> str | None:
    """Decrypt text encoded in an image

    If the message end is not found, `None`  is returned.
    """
    cols = image.size[0]
    end_length = len(encrypt.END_TEXT)
    # For last 3 bits
    modulus = 8
    decrypt = []
    endpoint = -end_length
    sequence = list(encrypt.END_TEXT)

    for pixel in (
        (
            n % cols,
            n // cols,
        )
        for n in range(image.size[0] * image.size[1])
    ):
        value = 0
        # Recover ASCII code
        for i, plane in enumerate(image.getpixel(pixel)[:3]):
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


def random_message(alphabet, length: int) -> str:
    """
    Generate random characters of a certain length

    param length: Number of characters to select.
    """
    return "".join(choices(alphabet, k=length))


def encrypt_decrypt(message: str, image: Image.Image) -> None:
    """Confirm that a message can be encrypted in an image and recovered"""
    encryption = encrypt.encrypt_text_to_image(message, image)
    assert encryption
    decrypted, _ = decrypt.decrypt_text_from_image(encryption)
    assert utility.strip_non_ascii(message.strip()) == decrypted


def too_long(image: Image.Image):
    """Should return `None` if message too long to encrypt"""
    extent = pixel_count(image)
    message = "a" * (extent + 1)
    result = encrypt.encrypt_text_to_image(message, image)
    assert result is None


def verify(alphabet: str, length: int, image: Image.Image) -> None:
    """Generates a random message of a given length and confirm that it encrypts and decrypts correctly."""
    message = random_message(alphabet, length)
    encrypt_decrypt(message, image)


def test_messages() -> None:
    """Checks encrypting-decrypting for messages of various lengths"""
    for file in images:
        # No RGBA!
        image = Image.open(file).convert("RGB")
        print(file)
        for length in (0, 1, 5, 10, 100, 1000, 5000, pixel_count(image) - end_length):
            extent = image.size[0] * image.size[1]
            too_long(image)
            if length <= extent:
                verify(ascii, length, image)
                verify(combined, length, image)
