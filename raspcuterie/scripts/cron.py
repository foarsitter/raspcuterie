#!/usr/bin/env /home/pi/.virtualenvs/raspcuterie/bin/python
import sys

sys.path.extend(['/home/pi/raspcuterie-pi', '/home/pi/raspcuterie-pi'])

import Adafruit_DHT

from raspcuterie.db import insert_humidity, insert_temperature
from raspcuterie.devices import AM2302


def log_am2302():
    humidity, temperature = Adafruit_DHT.read_retry(AM2302.sensor, AM2302.pin)

    insert_humidity(humidity)
    insert_temperature(temperature)

    print("am2302 values insert to the database")


log_am2302()