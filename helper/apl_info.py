from dataclasses import dataclass
from enum import Enum


@dataclass
class APLInfo:
    make = "APL"
    model = ""
    artist = "Davr, Jaavv, maxence, standard_effect"
    software = "A Pixel Life"
    description = "Python Discord Summer Code Jam 2023 - The Thick Wrappers Project"

    def set_model(self, value) -> None:
        width, height = 0, 1
        self.model = f"A{value[width]}P{value[height]}L"


class APLExif(Enum):
    MAKE = 271
    MODEL = 272
    ARTIST = 315
    SOFTWARE = 305
    DESCRIPTION = 270
