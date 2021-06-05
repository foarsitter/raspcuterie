from pathlib import Path
from typing import Dict

import yaml

from raspcuterie import base_path
from raspcuterie.config.schema import RaspcuterieConfigSchema
from raspcuterie.devices import InputDevice
from raspcuterie.devices.control import ControlRule
from raspcuterie.devices.output.relay import OutputDevice


def read_config_as_yaml(file: Path) -> Dict:
    InputDevice.discover()
    OutputDevice.discover()

    data = file.read_text()

    data_loaded = yaml.safe_load(data)
    data_loaded["raw"] = data
    return data_loaded


def register_input_devices(config: RaspcuterieConfigSchema, logger):
    for device in config.devices:
        if device.type in InputDevice.types:
            device_class = InputDevice.types[device.type]
        elif device.type in OutputDevice.types:
            device_class = OutputDevice.types[device.type]
        else:
            device_class = None

        if not device_class:
            logger.error(f"Cloud not initiate {device}")
        else:
            kwargs = device.dict()
            del kwargs["type"]
            del kwargs["name"]

            device_class(device.name, **kwargs)


def register_config_rules(config: RaspcuterieConfigSchema):
    control_rules = config.control

    for group_name, control_group in control_rules.items():

        for device_name, rules in control_group.rules.items():

            device = OutputDevice.registry[device_name]
            for rule in rules:
                ControlRule(
                    device,
                    expression=rule.expression,
                    action=rule.action,
                    name=rule.rule,
                )


def get_config_file(app) -> Path:
    if app.debug or app.testing:
        file = Path(__file__).parent.parent.parent / "config_dev.yaml"
    else:

        file = base_path / "config.yaml"

    return file


def setup(app):
    file = get_config_file(app)
    config = read_config_as_yaml(file)

    app.logger.info(f"Loading config {file}")

    RaspcuterieConfigSchema.update_forward_refs()

    app.schema = RaspcuterieConfigSchema.parse_obj(config)
    app.config["config"] = config["raw"]
    register_input_devices(app.schema, app.logger)
    register_config_rules(app.schema)
