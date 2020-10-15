import random

from gpiozero import LED

from raspcuterie import FAKE_VALUES


class RelayManager:
    def __init__(self):
        try:
            self.relay_4 = LED("GPIO6")
            self.relay_3 = LED("GPIO13")
            self.relay_2 = LED("GPIO19")
            self.relay_1 = LED("GPIO26")
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

        if FAKE_VALUES:
            return random.choice([True, False])

        return bool(self.relays[index].value)


manager = RelayManager()
