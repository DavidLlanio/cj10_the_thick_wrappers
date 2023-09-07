from PIL.Image import Image

from .utility import get_pixels_from_image


def decrypt_text_from_image(img) -> tuple:
    """Iterates and checks every binary RGB triplet, scanning over the LSB"""
    delimiter = False
    pixel_list, word_total = [], ""
    RGB_binary_list = get_pixels_from_image(img)

    # Iterates through each pixel's binary values and concatenates the least significant bits into decoded code
    for pixel in RGB_binary_list:
        output = "0"
        r, g, b = pixel[0][-3:], pixel[1][-3:], pixel[2][-1]
        output = output + (str(b) + str(g) + str(r))
        pixel_list.append(int(output, 2))

    # Iterates through each binary output and converts each binary to ASCII, simultaneously checking for the delimiter
    for binary in pixel_list:
        if word_total[-5:] == ",,,..":
            delimiter = True
            break
        word_total += format(binary, "c")
    return word_total[:-5], delimiter


def decrypt_image_from_image(image: Image) -> Image:
    """Decrypt the secret image from the given input image"""
    return image.point(lambda byte: (byte & 0b00001111) << 4)
