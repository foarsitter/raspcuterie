import logging
import time

from flask import current_app
from timeout_decorator import timeout

from raspcuterie import version
from raspcuterie.cli import cli, with_appcontext
from raspcuterie.devices import InputDevice, OutputDevice
from raspcuterie.devices.control import ControlRule
from raspcuterie.gpio import GPIO


def evaluate_config_rules(context):
    for rule in ControlRule.registry:
        try:
            rule.execute_if_matches(context)
        except Exception as e:
            current_app.logger.exception(e)


@cli.command(short_help="Log the input and output devices")
@with_appcontext
@timeout(30)
def log():
    current_app.logger.info(version)

    current_app.logger.setLevel(logging.DEBUG)

    secure_pin = 24
    current_app.logger.info(f"Setting {secure_pin} to HIGH to activate the AM2302")

    GPIO.setup(secure_pin, GPIO.OUT)
    GPIO.output(secure_pin, GPIO.HIGH)

    time.sleep(1)

    context = ControlRule.context()

    evaluate_config_rules(context)

    for input_device in InputDevice.registry.values():
        try:
            input_device.log()
        except Exception as e:
            current_app.logger.exception(e)

    for output_device in OutputDevice.registry.values():
        try:
            output_device.log()
        except Exception as e:
            current_app.logger.exception(e)

    GPIO.output(24, GPIO.LOW)

    current_app.logger.info(f"Setting {secure_pin} to LOW to disable the AM2302")


if __name__ == "__main__":
    log()
