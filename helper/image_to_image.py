import numpy as np
from PIL import Image

from StegaImage import StegaImage
from helper.Pixel import Pixel


def load_image(directory: str):
    img = Image.open(directory)
    return StegaImage(img)


def steganographize(cover: StegaImage, secret: StegaImage, output: str) -> None:
    height, width, mode = cover.image_as_array.shape
    cover_msb = cover.get_image_msb()
    secret_msb = secret.get_image_msb()
    stega_image = np.empty((height, width), dtype=object)
    for y in range(height):
        for x in range(width):
            stega_image[y, x] = merge_sb(cover_msb[y, x], secret_msb[y, x])
    stega = Image.fromarray(stega_image, mode='RGB')
    stega.save(output)


def merge_sb(msb: tuple[str, str, str], lsb: [str, str, str]):
    sb = msb[0] + lsb[0], msb[1] + lsb[1], msb[2] + lsb[2]
    return np.array(Pixel.tuple_input(sb).get_rgb(), dtype='uint8')


if __name__ == "__main__":
    with Image.open("../.test_folder/rgb.png") as image:
        cover_image = StegaImage(image)
        bbb = image.split()
        secret_image = load_image("../.test_folder/rgb2.png")
        print("Steganographizing...")
        steganographize(cover_image, secret_image, "../.test_folder/output.png")
        print("Complete!")
