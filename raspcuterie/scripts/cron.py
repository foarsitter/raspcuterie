import sys

import click

from raspcuterie.cli import cli

sys.path.extend(["/home/pi/raspcuterie-pi", "/home/pi/raspcuterie-pi"])

from raspcuterie.devices.relay import manager
from raspcuterie.devices.hx711 import hx

from raspcuterie.db import (
    insert_humidity,
    insert_temperature,
    insert_relay,
    insert_weight,
)
from raspcuterie.devices.am2302 import AM2302


@cli.command()
def log_values():
    humidity, temperature = AM2302.read()

    insert_humidity(humidity)
    insert_temperature(temperature)
    insert_relay(manager.is_on(1), manager.is_on(2), manager.is_on(3), manager.is_on(4))
    insert_weight(hx.get_grams())
    print("Values insert to the database")
