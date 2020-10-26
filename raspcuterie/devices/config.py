from typing import List

from raspcuterie.devices import InputDevice
from raspcuterie.devices.relay import OutputDevice


class ConfigRule:
    registry: List["ConfigRule"] = []

    def __init__(self, device: OutputDevice, expression: str, action: str, name: str = None):
        ConfigRule.registry.append(self)
        self.name = name
        self.device: OutputDevice = device
        self.expression: str = expression
        self.action: str = action

    def context(self):
        context = {}

        for device in InputDevice.registry.values():
            context.update(device.get_context())

        return context

    def matches(self):
        return eval(self.expression, self.context())

    def execute(self):
        action = getattr(self.device, self.action)
        return action()

    def execute_if_matches(self):
        if self.matches():
            print(f"Matches expression: {self.expression}")
            print(f"Executing {self.name}.{self.action}")
            return self.execute()
        else:
            print(f"Does not match expression: {self.expression}")
