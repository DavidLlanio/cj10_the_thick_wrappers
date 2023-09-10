import string
from random import choices, seed

from PIL import Image

from helper import decrypt, encrypt, utility

seed(a=1)
ascii = string.ascii_letters + string.digits + string.punctuation + "\n\t\r"
non_ascii = "".join(map(chr, range(128, 1000)))
combined = ascii + non_ascii
end_length = len(encrypt.END_TEXT)

img_dir = "static"


def pixel_count(image: Image.Image) -> int:
    """Gets the number of pixels in an image."""
    return image.size[0] * image.size[1]


def random_message(alphabet, length: int) -> str:
    """Generates random characters of a certain length."""
    return "".join(choices(alphabet, k=length))


def encrypt_decrypt(message: str, image: Image.Image) -> None:
    """Confirms that a message can be encrypted in an image and recovered"""
    encryption = encrypt.encrypt_text_to_image(message, image)
    assert encryption
    decrypted, _ = decrypt.decrypt_text_from_image(encryption)
    assert utility.strip_non_ascii(message.strip()) == decrypted


def too_long(image: Image.Image) -> None:
    """Verifies that encryption fails on an image if the message is too long to encrypt"""
    extent = pixel_count(image)
    message = "a" * (extent + 1)
    result = encrypt.encrypt_text_to_image(message, image)
    assert result is None


def verify(alphabet: str, length: int, image: Image.Image) -> None:
    """Generates and tests a random message of a given length"""
    message = random_message(alphabet, length)
    encrypt_decrypt(message, image)


def test_messages(all_images) -> None:
    """Checks encrypting-decrypting for messages of various lengths"""
    for file in all_images:
        image = Image.open(file)
        for length in (0, 1, 5, 10, 100, 1000, 5000, pixel_count(image) - end_length):
            extent = image.size[0] * image.size[1]
            too_long(image)
            if length <= extent:
                verify(ascii, length, image)
                verify(combined, length, image)
