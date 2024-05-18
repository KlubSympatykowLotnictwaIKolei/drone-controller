from enum import Enum

"""
Enums to showing options available in pylon software for certain parameters.
Options supported by following cameras are included:
 - Basler ace2 a2A2448-75ucBAS
"""

class ExposureAutoValues(Enum):
    OFF = "Off"
    ONCE = "Once"
    CONTINUOUS = "Continuous"

class PixelFormatValues(Enum):
    Mono8 = "Mono8"
    Mono10 = "Mono10"
    Mono10p = "Mono10p"
    Mono12 = "Mono12"
    Mono12p = "Mono12p"
    BayerRG8 = "BayerRG8"
    BayerRG10 = "BayerRG10"
    BayerRG10p = "BayerRG10p"
    BayerRG12 = "BayerRG12"
    BayerRG12p = "BayerRG12p"
    RGB8 = "RGB8"
    BGR8 = "BGR8"
    YCbCr422_8 = "YCbCr422_8"
