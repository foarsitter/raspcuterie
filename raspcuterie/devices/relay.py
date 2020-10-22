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

        self.pin_number = bmc_number

        GPIO.setup(self.pin_number, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin_number, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin_number, GPIO.LOW)

    @property
    def value(self):
        return GPIO.input(self.pin_number)


class RelayManager:
    def __init__(self):
        try:
            self.relay_4 = ReplaySwitch("Relay4", 6)
            self.relay_3 = ReplaySwitch("Relay3", 13)
            self.relay_2 = ReplaySwitch("Relay2", 19)
            self.relay_1 = ReplaySwitch("Relay1", 26)
            self.relays = {
                1: self.relay_1,
                2: self.relay_2,
                3: self.relay_3,
                4: self.relay_4,
            }
        except Exception as e:
            if not FAKE_VALUES:
                raise e

    def is_on(self, index: int) -> bool:

        # if FAKE_VALUES:
        #     return random.choice([True, False])

        return bool(self.relays[index].value)


manager = RelayManager()
