from PIL.Image import Image

from .utility import parse_exif, pixels_to_binary


def decrypt_text_from_image(img: Image) -> tuple[str, bool]:
    """
    Decrypts an image encoded with text.

    param img: A Pillow Image object containing message
    This function iterates over an image's pixels and extracts the three least
    significant bits of each color plane. These values are summed and converted
    to the corresponding ASCII character. The function scans until it finds
    the message delimiter ",,,.." or it processes all pixels. It returns
    a tuple of the decrypted message and a bool indicating whether the
    delimiter (present in all valid messages) was found.
    """
    delimiter = False
    pixel_list, word_total = [], ""
    RGB_binary_list = pixels_to_binary(img)

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
    if size := parse_exif(image.getexif()):
        width, height = size
        image = image.crop((0, 0, width, height))
    else:
        print("WARNING: Could not parse size from EXIF metadata, falling back to decrypting whole image")

    return image.point(lambda byte: (byte & 0b00001111) << 4)
