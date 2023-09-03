from enum import Enum
from PIL import Image
from helper.Stega import Stega

import numpy as np


class StegaImage(Enum):
    CARRIER = 1
    COVER = 2


def load_image_sb(directory: str, img_type: StegaImage):
    img = Image.open(directory)
    image = Stega(img)
    # redundant
    match img_type:
        case StegaImage.COVER:
            return image.get_msb()
        case StegaImage.CARRIER:
            return image.get_msb()


def msb_to_lsb(cover_rgba, carrier_rgba):
    return cover_rgba[0] + carrier_rgba[0], cover_rgba[1] + carrier_rgba[1], cover_rgba[2] + carrier_rgba[2], \
           cover_rgba[3] + carrier_rgba[3]


def image_to_image(cover, carrier):
    steg_image = np.empty(cover.shape, dtype=object)
    for y in range(cover.shape[0]):
        for x in range(cover.shape[1]):
            steg_image[y, x] = cover[y, x][0] + carrier[y, x][0], cover[y, x][1] + carrier[y, x][1], cover[y, x][2] + \
                               carrier[y, x][2], cover[y, x][
                                   3] + carrier[y, x][3]
    return steg_image


if __name__ == "__main__":
    pass
