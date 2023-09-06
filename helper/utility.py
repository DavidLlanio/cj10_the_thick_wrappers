def get_pixels_from_image(img) -> list:
    """Translates an inputted image's pixels to binary"""
    pixels = img.load()
    width, height = img.size
    pixellist = []

    # Iterates through all of the picture's pixels, left to right then down
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            r, g, b = str(bin(r))[2:].zfill(8), str(bin(g))[2:].zfill(8), str(bin(b))[2:].zfill(8)
            pixellist.append((r, g, b))
    return pixellist


def clear_least_significant_bits(bits):
    """Function that will clear the given amount of least significant bits"""
    pass


def set_least_significant_bits(bits, content):
    """Function that will set the given least significant bits to content"""
    pass
