from PIL import Image

ASCII_MAX = 127
# Added as message end
PADDING = list(map(ord, ",,,.."))


# Convert string to bytes, removing non-ASCII characters
def strip_non_ascii(text: str) -> list[int]:
    """Convert string to bytes, removing non-ASCII characters"""
    result = []
    for char in text:
        if ((byte := ord(char)) <= ASCII_MAX):
            result.append(byte)
    return result


def encrypt_text(text: str, image_path: str) -> Image.Image:
    """Encode a text string in randomly selected coordinates of an image"""
    with Image.open(image_path) as image:
        # Convert to ASCII and add padding indicating message end
        bytes = strip_non_ascii(text)
        n = len(bytes)
        rows, cols = image.size

        extent = rows * cols
        if n > extent:
            raise ValueError(f"Cannot encode {n} characters in image of {extent} pixels")
        # Pixel coordinates, going left and down
        targets = [(c // cols, c % cols) for c in range(n)]

        # Alter 3 LSBs for each target pixel
        bit_length = 3
        modulus = 2 ** bit_length

        for target, byte in zip(targets, bytes):
            pixel: list[int] = image.getpixel(target)
            pixel = list(pixel)

            for i, plane in enumerate(pixel):
                # Clear 3 LSB
                plane >>= bit_length
                plane <<= bit_length
                pixel[i] = plane + byte % modulus
                byte >>= bit_length
            image.putpixel(target, tuple(pixel))

        # Save original values?
        return image
