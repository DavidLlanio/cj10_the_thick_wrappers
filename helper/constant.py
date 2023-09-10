from enum import Enum

SOFTWARE_TITLE = "In Plain Pixel"
TEAM_MEMBERS = "Davr, Jaavv, maxence, standard_effect"
DESCRIPTION = "Python Discord Summer Code Jam 2023 - The Thick Wrappers Project"
EXIF_MAKE = "IPP"
STARTING_X = 0
STARTING_Y = 0
BITS_4 = 4
# R, G, B
N_PLANES = 3

UI_STRINGS = {
    "crypt_type": ["Encrypt", "Decrypt"],
    "secret_type": ["Text", "Image"],
    "text_type": ["Text", "Text File"],

}


class ResizeMode(Enum):
    """Enumeration for flag to shrink or leave image as is"""

    DEFAULT = 0
    SHRINK_TO_SCALE = 1


class Sizing(Enum):
    """Enumeration for flags on difference in secret image and cover image"""

    SMALLER = 0
    BIGGER = 1
    TALLER = 2
    WIDER = 3


class Direction(Enum):
    """Enumeration for direction of bit shift"""

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class ExifData(Enum):
    """Enumeration for metadata locations"""

    MAKE = 271
    MODEL = 272
    ARTIST = 315
    SOFTWARE = 305
    DESCRIPTION = 270


class CrypType(Enum):
    ENCRYPT = 0
    DECRYPT = 1


class FileType(Enum):
    TEXT = 0
    IMAGE = 1


class TextType(Enum):
    TEXT = 0
    TEXT_FILE = 1
