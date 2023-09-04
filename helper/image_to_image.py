import copy

from PIL import Image

from helper.StegaImage import StegaImage


def load_image(directory: str):
    img = Image.open(directory)
    return StegaImage(img)


def steganograpize(cover: StegaImage, secret: StegaImage) -> StegaImage:
    secret_msb = secret.get_image_msb()
    stega_image = copy.deepcopy(cover)
    height, width, mode = stega_image
    for x in range(width):
        for y in range(height):
            stega_image.set_pixel_lsb((x, y), secret_msb[y, x])
    return stega_image


if __name__ == "__main__":
    with Image.open("../.test_folder/discord_logo.png") as image:
        cover_image = StegaImage(image)
        secret_image = load_image("../.test_folder/secret_test.png")
        stega_image = steganograpize(cover_image, secret_image)
