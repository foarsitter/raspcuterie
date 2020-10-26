import yaml

from raspcuterie import base_path
from raspcuterie.devices import InputDevice
from raspcuterie.devices.config import ConfigRule
from raspcuterie.devices.relay import OutputDevice


def parse_config():

    file = base_path / "config.yaml"

    from raspcuterie.devices.am2302 import SinusInput, AM2302  # noqa
    from raspcuterie.devices.hx711 import HX711  # noqa

    with file.open() as f:
        data_loaded = yaml.safe_load(f)

        return data_loaded


def register_input_devices(config):

    input_devices = config["devices"]["input"]

    for device in input_devices:

        if device["name"] in InputDevice.types:
            device_type = InputDevice.types[device["name"]]

            device_type(device["name"])
        else:
            print(f"Cloud not initiate {device}")


def register_output_devices(config):

    input_devices = config["devices"]["output"]

    for device in input_devices:
        device_name = device["name"]
        device_type = device.get("type", device_name)
        device_gpio = device["gpio"]

        device_class = OutputDevice.types[device_type]
        device_class(device_name, device_gpio)


def register_config_rules(config):

    config_rules = config["config"]

    for device, rules in config_rules.items():

        device = OutputDevice.registry[device]

        for rule in rules:

            ConfigRule(device, expression=rule["expression"], action=rule["action"], name=rule["rule"])
