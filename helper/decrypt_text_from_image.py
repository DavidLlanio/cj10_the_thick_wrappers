def convert_pixels_to_binary(img):
    """Translates an inputted image's pixels to binary"""
    pixels = img.load()
    width, height = img.size
    pixellist = []

    # Iterates through all of the picture's pixels, left to right then down
    def pixel_list():
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                r, g, b = str(bin(r))[2:].zfill(8), str(bin(g))[2:].zfill(8), str(bin(b))[2:].zfill(8)
                pixellist.append((r, g, b))
        return pixellist
    return pixel_list()


def binary_decoder(img):
    """Iterates and checks every binary RGB triplet, scanning over the LSB"""
    delimiter = False
    pixel_list, word_total = [], ""
    RGB_binary_list = convert_pixels_to_binary(img)

    # Iterates through each pixel's binary values and concatenates the least significant bits into decoded code
    for pixel in RGB_binary_list:
        output = "0"
        r, g, b = pixel[0][-3:], pixel[1][-3:], pixel[2][-1]
        output = output + (str(b) + str(g) + str(r))
        pixel_list.append(int(output, 2))

    # Iterates through each binary output and converts each binary to ASCII
    for binary in pixel_list:
        if word_total[-5:] == ",,,..":
            delimiter = True
            break
        word_total += format(binary, "c")
    return word_total[:-5], delimiter
