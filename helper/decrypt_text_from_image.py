def all_pixels_to_binary(img):
    """Translates an inputted image's pixels to binary"""
    pixels = img.load()
    width, height = img.size
    pixellist = []

    def pixel_to_bin(x, y):
        r, g, b = pixels[x, y]
        r, g, b = str(bin(r))[2:].zfill(8), str(bin(g))[2:].zfill(8), str(bin(b))[2:].zfill(8)
        return r, g, b

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
    delimiter = False
    pixel_list = []
    RGB_binary_list = all_pixels_to_binary(img)
    word_total = ""
    for pixel in RGB_binary_list:
        output = "0"
        r, g, b = pixel[0][-3:], pixel[1][-3:], pixel[2][-1]
        output = output + (str(b) + str(g) + str(r))
        pixel_list.append(output)
    for binary in pixel_list:
        if word_total[-5:] == ",,,..":
            delimiter = True
            break
        word_total += bin_to_ascii(binary)
    return word_total[:-5], delimiter


def bin_to_ascii(binary):
    """Traslates inputted binary to ASCII"""
    ascii = int(f"{(binary)}", 2)
    byte_number = (ascii.bit_length() + 7) // 8
    binary_array = ascii.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()
    return ascii_text
