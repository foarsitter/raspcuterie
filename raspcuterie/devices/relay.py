import datetime
from builtins import super
from typing import Dict, Type

from raspcuterie.gpio import GPIO


class OutputDevice:
    type: str
    registry: Dict[str, "OutputDevice"] = {}
    types: Dict[str, Type["OutputDevice"]] = {}

    def __init__(self, name):
        OutputDevice.registry[name] = self
        self.name = name

    def __init_subclass__(cls, **kwargs):
        super(OutputDevice, cls).__init_subclass__(**kwargs)
        OutputDevice.types[cls.type] = cls


class RelaySwitch(OutputDevice):
    type = "relay"

    def __init__(self, name, bmc_number):
        super(RelaySwitch, self).__init__(name)

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

        self.relay_4 = RelaySwitch("relay4", 6)
        self.relay_3 = RelaySwitch("relay3", 13)
        self.relay_2 = RelaySwitch("relay2", 19)
        self.relay_1 = RelaySwitch("relay1", 26)
        self.relays = {
            1: self.relay_1,
            2: self.relay_2,
            3: self.relay_3,
            4: self.relay_4,
        }

    def is_on(self, index: int) -> bool:
        return bool(self.relays[index].value)

    def heater(self):
        return self.relay_4

    def refrigerator(self):
        return self.relay_1

    def humidifier(self):
        return self.relay_3

    def dehumidifier(self):
        return self.relay_2


manager = RelayManager()
