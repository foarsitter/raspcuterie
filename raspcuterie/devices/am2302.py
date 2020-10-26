import datetime
import math

import random

from raspcuterie import FAKE_VALUES
from raspcuterie.devices import InputDevice


class AM2302(InputDevice):
    type = "AM2303"

    def read(self):
        if FAKE_VALUES:
            return random.randint(0, 100), random.randint(5, 25)
        return self._read_am2303()

    def _read_am2303(self):

        import Adafruit_DHT

        sensor = Adafruit_DHT.DHT22

        pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin, delay_seconds=0.2)

        return round(humidity, 2), round(temperature, 2)

    def get_context(self):

        humidity, temperature = self.read()

        return dict(humidity=humidity, temperature=temperature)


class SinusInput(InputDevice):
    type = "sinus"
    radial = math.pi / 180

    def sinus(self, lower=5, upper=25):

        delta = upper - lower
        middle = lower + delta / 2

        return (
            middle
            + math.sin(datetime.datetime.utcnow().minute * 6 * SinusInput.radial)
            + delta / 2
        )

    def read(self):
        return self.sinus()

    def get_context(self):
        return dict(humidity=self.sinus(60, 100), temperature=self.sinus())
