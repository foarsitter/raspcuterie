import datetime
from typing import Dict

from raspcuterie.gpio import GPIO

from raspcuterie import FAKE_VALUES


class OutputDevice:
    _registry: Dict[str, "OutputDevice"] = {}

    def __init__(self, name):
        OutputDevice._registry[name] = self
        self.name = name


class ReplaySwitch(OutputDevice):
    def __init__(self, name, bmc_number):
        super(ReplaySwitch, self).__init__(name)

        self.last_witch = datetime.datetime.now() - datetime.timedelta(seconds=60)

        self.pin_number = bmc_number
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.OUT)

    def on(self):
        if self.last_witch < datetime.datetime.now() - datetime.timedelta(seconds=60):
            GPIO.output(self.pin_number, GPIO.HIGH)
            self.last_witch = datetime.datetime.now()
        else:
            print("timeout")

    def off(self):
        GPIO.output(self.pin_number, GPIO.LOW)

    @property
    def value(self):
        return GPIO.input(self.pin_number)


class RelayManager:

    def __init__(self):

        self.relay_4 = ReplaySwitch("relay4", 6)
        self.relay_3 = ReplaySwitch("relay3", 13)
        self.relay_2 = ReplaySwitch("relay2", 19)
        self.relay_1 = ReplaySwitch("relay1", 26)
        self.relays = {
            1: self.relay_1,
            2: self.relay_2,
            3: self.relay_3,
            4: self.relay_4,
        }

    def is_on(self, index: int) -> bool:
        return bool(self.relays[index].value)


manager = RelayManager()
