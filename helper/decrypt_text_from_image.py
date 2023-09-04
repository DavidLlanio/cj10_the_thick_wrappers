from PIL import Image


def all_pixels_to_binary(img):
    """Translates an inputted image's pixels to binary"""
    pixels = img.load()
    width, height = img.size
    pixellist = []

    def pixel_to_bin(x, y):
        if img.mode == 'RGBA':
            r, g, b, a = pixels[x, y]
            r, g, b = int(str(bin(r))[2:]), int(str(bin(g))[2:]), int(str(bin(b))[2:])
            return str(r), str(g), str(b)

        else:
            r, g, b = pixels[x, y]
            r, g, b = int(str(bin(r))[2:]), int(str(bin(g))[2:]), int(str(bin(b))[2:])
            return str(r), str(g), str(b)

    # Iterates through all of the picture's pixels, left to right then down
    def pixel_list():
        for y in range(height):
            for x in range(width):
                rgb_val = pixel_to_bin(x, y)
                pixellist.append(rgb_val)
    pixel_list()

    return pixellist


def binary_decoder(img):
    """Iterates and checks every binary RGB triplet, scanning over the last 3 LSB"""
    img = Image.open(img)
    pixel_list = []
    RGB_binary_list = all_pixels_to_binary(img)
    word_total = ""
    for pixel in RGB_binary_list:
        output = "0"
        a, b, c = pixel[0][-3:], pixel[1][-3:], pixel[2][-1]
        output = output + (str(a) + str(b) + str(c))
        pixel_list.append(output)
    pixel_list.append("0010110000101100001011000010111000101110")  # forces a delimter incase one wasn't encrypted in
    while word_total[-5:] != ",,,..":
        for binary in pixel_list:
            word_total += bin_to_ascii(binary)
    return word_total


def bin_to_ascii(binary):
    """Traslates inputted binary to ASCII"""
    ascii = int(f"{(binary)}", 2)
    byte_number = ascii.bit_length() + 7 // 8
    binary_array = ascii.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()
    return ascii_text
