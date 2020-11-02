from flask import current_app
from flask.cli import with_appcontext

from raspcuterie.cli import cli
from raspcuterie.config import setup
from raspcuterie.devices import InputDevice, OutputDevice
from raspcuterie.devices.control import ControlRule


def evaluate_config_rules():
    for rule in ControlRule.registry:
        rule.execute_if_matches()


@cli.command()
@with_appcontext
def log_values():
    setup(current_app)
    evaluate_config_rules()

    for input_device in InputDevice.registry.values():
        input_device.log()

    for output_device in OutputDevice.registry.values():
        output_device.log()


if __name__ == "__main__":
    log_values()
