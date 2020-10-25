import click

from raspcuterie.cli import cli
from raspcuterie.db import (
    insert_humidity,
    insert_temperature,
    insert_relay,
    insert_weight,
)
from raspcuterie.devices.am2302 import AM2302
from raspcuterie.devices.config import ConfigRule
from raspcuterie.devices.hx711 import hx
from raspcuterie.devices.relay import manager


def evaluate_config_rules():

    ConfigRule(
        manager.dehumidifier(),
        expression="humidity > 75",
        action="on",
        name="dehumidifier",
    ).execute_if_matches()

    ConfigRule(
        manager.dehumidifier(),
        expression="humidity < 65",
        action="off",
        name="dehumidifier",
    ).execute_if_matches()

    ConfigRule(
        manager.humidifier(),
        expression="humidity > 70",
        action="off",
        name="humidifier",
    ).execute_if_matches()

    ConfigRule(
        manager.humidifier(),
        expression="humidity < 60",
        action="on",
        name="humidifier",
    ).execute_if_matches()

    ConfigRule(
        manager.refrigerator(),
        expression="temperature > 15",
        action="on",
        name="refrigerator",
    ).execute_if_matches()

    ConfigRule(
        manager.refrigerator(),
        expression="temperature < 13",
        action="off",
        name="refrigerator",
    ).execute_if_matches()

    ConfigRule(
        manager.heater(),
        expression="temperature < 12",
        action="on",
        name="heater",
    ).execute_if_matches()

    ConfigRule(
        manager.heater(),
        expression="temperature > 15",
        action="off",
        name="heater",
    ).execute_if_matches()


@cli.command()
def log_values():
    humidity, temperature = AM2302.read()

    evaluate_config_rules()

    insert_humidity(humidity)
    insert_temperature(temperature)
    insert_relay(manager.is_on(1), manager.is_on(2), manager.is_on(3), manager.is_on(4))
    insert_weight(hx.get_grams())


if __name__ == "__main__":
    log_values()
