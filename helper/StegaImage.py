from PIL import Image

import numpy as np


class StegaImage:
    """ Pillow.Image delegate wrapper """

    def __init__(self, image: Image.Image):
        self.image = image
        self._image_as_array = np.asarray(image)

    def get_image_array(self) -> np.ndarray:
        """ Return image as numpy array value """
        return self._image_as_array

    def _update_image(self) -> None:
        """ Convert array back to Image object """
        self.image = Image.fromarray(self._image_as_array)

    def reset_lsb(self) -> None:
        """ Logical shift each pixel 4 bits to the right and back """
        bits = 4
        self._image_as_array = (self._image_as_array >> bits) << bits
        self._update_image()

    def reset_msb(self) -> None:
        """ Logical shift each pixel 4 bits to the right """
        bits = 4
        self._image_as_array = self._image_as_array >> bits
        self._update_image()
