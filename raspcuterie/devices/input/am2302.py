import datetime
import math

from raspcuterie import db
from raspcuterie.devices import InputDevice
from raspcuterie.utils import time_based_sinus


class AM2302(InputDevice):
    type = "AM2303"

    def read(self):
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

    def sinus(self, lower, upper):
        return time_based_sinus(datetime.datetime.now().minute, lower, upper)

    def read(self):
        return self.sinus(60, 100), self.sinus(5, 25)

    def get_context(self):
        return dict(humidity=self.sinus(60, 100), temperature=self.sinus(5, 25))

    def get_grams(self):
        return self.sinus(50, 100)

    def log(self):
        humidity, temperature = self.read()

        db.insert_humidity(humidity)
        db.insert_temperature(temperature)
