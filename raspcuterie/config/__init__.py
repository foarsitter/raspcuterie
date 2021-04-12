from pathlib import Path

import yaml
from flask import current_app, g

from raspcuterie import base_path

# from raspcuterie.config.schema import RaspcuterieConfigSchema
from raspcuterie.devices import InputDevice
from raspcuterie.devices.control import ControlRule
from raspcuterie.devices.output.relay import OutputDevice


def parse_config(file: Path):

    InputDevice.discover()
    OutputDevice.discover()

    data = file.read_text()

    data_loaded = yaml.safe_load(data)
    data_loaded["raw"] = data
    return data_loaded


def register_input_devices(config: RaspcuterieConfigSchema):

    for device in config.devices:
        if device.type in InputDevice.types:

            device_class = InputDevice.types[device.type]
        elif device.type in OutputDevice.types:
            device_class = InputDevice.types[device.type]
        else:
            device_class = None

        if not device_class:
            current_app.logger.error(f"Cloud not initiate {device}")
        else:
            kwargs = device.dict()
            del kwargs["type"]

            device_class(device.name, **kwargs)


def register_config_rules(config):

    control_rules = config["control"]

    for device, rules in control_rules.items():

        device = OutputDevice.registry[device]

        for rule in rules:

            ControlRule(
                device,
                expression=rule["expression"],
                action=rule["action"],
                name=rule["rule"],
            )


def get_config_file(app) -> Path:
    if app.debug or app.testing:
        file = Path(__file__).parent.parent.parent / "config_dev.yaml"
    else:

        file = base_path / "config.yaml"

    return file


def setup(app):
    file = get_config_file(app)
    config = parse_config(file)

    # g.config = RaspcuterieConfigSchema.parse_raw(config)

    app.config["config"] = config["raw"]

    register_input_devices(config)
    register_config_rules(config)
