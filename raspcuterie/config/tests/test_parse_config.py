from pathlib import Path

import raspcuterie
from raspcuterie.devices.control import ControlRule
from raspcuterie.devices.output.relay import OutputDevice

from raspcuterie.config import (
    parse_config,
    register_input_devices,
    register_config_rules, RaspcuterieConfigSchema,
)
from raspcuterie.devices import InputDevice


def test_parse_config():
    file = raspcuterie.lib_path / "config_dev.yaml"

    ControlRule.registry = []

    x = parse_config(file)

    x = RaspcuterieConfigSchema.parse_obj(x)

    assert x

    register_input_devices(x, None)

    assert len(InputDevice.registry) == 2

    assert len(OutputDevice.registry) == 5

    register_config_rules(x)

    assert len(ControlRule.registry) == 4
