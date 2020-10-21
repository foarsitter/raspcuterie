import random

from raspcuterie import FAKE_VALUES


class AM2302:

    @staticmethod
    def read():
        if FAKE_VALUES:
            return random.randint(0, 100), random.randint(5, 25)
        return AM2302._read_am2303()

    @staticmethod
    def _read_am2303():

        import Adafruit_DHT

        sensor = Adafruit_DHT.DHT22

        pin = 4

        return Adafruit_DHT.read_retry(sensor, pin)