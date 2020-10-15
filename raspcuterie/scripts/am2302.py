#!/usr/bin/env /home/pi/.virtualenvs/raspcuterie/bin/python
import json
import sys
from pathlib import Path

import Adafruit_DHT

sys.path.extend(['/home/pi/raspcuterie-pi', '/home/pi/raspcuterie-pi'])

from raspcuterie import base_path
from raspcuterie.devices import AM2302

temperature_file = base_path / "temperature.json"
humidity_file = base_path / "humidity.json"


def append_file(file: Path, value: float):
    with file.open(mode="r") as f:
        data = json.load(f)
        if not data:
            data = []
        data.append(value)

    with file.open(mode="w") as f:
        json.dump(data, f)


humidity, temperature = Adafruit_DHT.read_retry(AM2302.sensor, AM2302.pin)

append_file(temperature_file, temperature)
append_file(humidity_file, humidity)
