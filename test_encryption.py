# Demonstrates encyption on a sample image
import string
from random import choices

from PIL import Image

from helper import encrypt_text

chars = string.ascii_letters + string.digits + string.punctuation


def random_message(length: int) -> str:
    """Generate random characters of a certain length

    param length: Number of characters to select.
    """
    return "".join(choices(chars, k=length))


def test_message(message: str, image: Image.Image) -> None:
    """Confirm a message is correctly encoded into an image.

    param message: String to encode.
    param image: Image in which to encode

    This function checks that `encrypt_text` returns a valid
    result if called with the given message and image. It
    then decodes the message and confirms that it is identical to the original
    text.
    """
    end_length = len(encrypt_text.END_TEXT)
    result = encrypt_text.encrypt_text(message, image)
    assert result and result != image

    cols = result.size[1]
    decrypt = []
    modulus = 8

    # Decode least significant bits in each pixel
    for pixel in [(n // cols, n % cols) for n in range(len(message) + end_length)]:
        value = 0
        for i, plane in enumerate(result.getpixel(pixel)):
            bits = plane % modulus
            bits <<= 3 * i
            value += bits
        decrypt.append(chr(value))
    # Combine characters and remove end-of-message padding
    decrypt = "".join(decrypt)[: len(decrypt) - end_length]
    assert decrypt == message.strip()


# Test different message sizes
# From https://www.rawpixel.com/image/7514064/photo-image-public-domain-galaxy-space
image = Image.open("nebula.jpeg")
for length in (0, 5, 100, 5000, 15000):
    message = random_message(length)
    test_message(message, image)

# Maximum length message
test_message("a" * 9995, image.crop((0, 0, 100, 100)))
# One char too many
assert encrypt_text.encrypt_text("a" * 9996, image.crop((0, 0, 100, 100))) is None
