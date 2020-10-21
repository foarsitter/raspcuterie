import time

import sys

sys.path.extend(["/home/pi/raspcuterie-pi", "/home/pi/raspcuterie-pi"])
from raspcuterie.devices.hx711.calibration import hx


CALI_OFFSET = 0
CALI_SCALE = 1

def setup():
    """
    code run once

    ffset:
Scale:
Item weighs 361.50437512749477 grams.


    """

    cali = 22

    x = []

    while True:

        if cali == CALI_OFFSET:
            hx.offset = 0
            hx.scale = 1
            y = hx.read()
        elif cali == CALI_SCALE:
            hx.scale = 1
            y = hx.read()
        else:
            y = hx.get_grams()

        x.append(y)
        # print("{0:.2f}".format(sum(x) / len(x)))
        print("{0:.2f}".format(y))
        time.sleep(0.1)


setup()
