from secrets import randbelow

from PIL import Image


def select_pixels(x: int, y: int, number: int) -> set[tuple[int, int]]:
    """Randomly select a given number of (x, y) coordinates for an image of given dimensions"""
    extent = x * y
    if number > extent:
        raise ValueError(f"Cannot encode {number} characters in image of {extent} pixels")
    chosen = set()

    # Randomly sample from range of valid 1D indices, then convert to 2D
    while len(chosen) < number:
        new = randbelow(extent)
        coord = (new // y, new % y)
        if coord not in chosen:
            chosen.add(coord)
    return chosen


def encrypt(text: str, image_path: str) -> tuple[Image.Image, dict[tuple[int, int], int]]:
    """Encode a text string in randomly selected coordinates of an image"""
    with Image.open(image_path) as image:
        bytes = map(ord, text)
        n = len(text)
        targets = select_pixels(*image.size, n)
        modulus = 8

        # Alter 3 LSBs for each target pixel
        originals = []
        for target, byte in zip(targets, bytes):
            print(target)
            pixel: list[int] = image.getpixel(target)
            originals.append(pixel)
            pixel = list(pixel)

            for i, plane in enumerate(pixel):
                plane >>= 3
                plane <<= 3
                pixel[i] = plane + byte % modulus
                byte >>= 3
            image.putpixel(target, tuple(pixel))

        # Save original values?
        image.show()
        return image, dict(zip(targets, originals))
