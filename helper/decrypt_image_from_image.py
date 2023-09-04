from PIL import Image as PILImage
from PIL.Image import Image

def _lsb_to_msb(byte: int) -> int:
    """Convert the least significant bits of the given byte into the most significant bits"""
    return (byte & 0b00001111) << 4

def decrypt_image(image: Image) -> Image:
    """Decrypt the secret image from the given input image"""
    r, g, b = image.split()
    r.point(_lsb_to_msb)
    g.point(_lsb_to_msb)
    b.point(_lsb_to_msb)

    return PILImage.merge("RGB", (r, g, b))
