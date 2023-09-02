from PIL import Image

image = ""  # TODO add image input here


def all_pixels_to_binary(image):
    """Translates an inputted image's pixels to binary"""
    img = Image.open(image)
    pixels = img.load()
    print(pixels)
    width, height = img.size
    pixellist = []

    def pixel_to_bin(x, y):
        if img.mode == 'RGBA':
            r, g, b, a = pixels[x, y]
            r, g, b = int(str(bin(r))[2:]), int(str(bin(g))[2:]), int(str(bin(b))[2:])
            return r, g, b

        else:
            r, g, b = pixels[x, y]
            r, g, b = int(str(bin(r))[2:]), int(str(bin(g))[2:]), int(str(bin(b))[2:])
            return r, g, b

    # Iterates through all of the picture's pixels, left to right then down
    def pixel_list():
        for y in range(height):
            for x in range(width):
                rgb_val = pixel_to_bin(x, y)
                pixellist.append(rgb_val)
    pixel_list()

    return pixellist


def binary_decoder(image):
    """Iterates and checks every binary RGB triplet, scanning over the last 3 LSB"""
    RGB_binary_list = all_pixels_to_binary(image)
    for pixel in RGB_binary_list:
        output = ""
        for y in pixel:
            y = str(y)
            output += y[-3:]
        print(bin_to_ascii(output))


def bin_to_ascii(binary):
    """Traslates inputted binary to ASCII"""
    ascii = int(f"{(binary)}", 2)
    byte_number = ascii.bit_length() + 7 // 8
    binary_array = ascii.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()
    return ascii_text
# example: print(bin_to_ascii(11000010110001001100011)) # "abc"
