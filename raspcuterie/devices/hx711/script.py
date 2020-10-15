import time

import sys
sys.path.extend(['/home/pi/raspcuterie-pi', '/home/pi/raspcuterie-pi'])
from raspcuterie.devices.hx711.calibration import hx


def setup():
    """
    code run once
    """
    hx.offset = 8436807.40

    w1 = 8284629.00

    w2 = 362

    hx.scale = (8284629.00 - hx.offset) / 362
    # hx.scale = 1

    x = []

    while True:
        y = hx.get_grams()
        x.append(y)
        print("{0:.2f}".format(sum(x) / len(x)))
        # print("{0:.2f}".format(y))
        time.sleep(0.1)

setup()