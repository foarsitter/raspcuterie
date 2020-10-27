from typing import List

from raspcuterie.devices import InputDevice
from raspcuterie.devices import OutputDevice


class ControlRule:
    registry: List["ControlRule"] = []

    def __init__(self, device: OutputDevice, expression: str, action: str, name: str = None):
        ControlRule.registry.append(self)
        self.name = name
        self.device: OutputDevice = device
        self.expression: str = expression
        self.action: str = action

    @staticmethod
    def context():
        context = {}

        for device in InputDevice.registry.values():
            context.update(device.get_context())

        return context

    def matches(self):
        return eval(self.expression, self.context())

    def execute(self):
        print(self.action)
        try:
            action = getattr(self.device, self.action)
            return action()
        except Exception as e:
            print(e)

    def execute_if_matches(self):
        if self.matches():
            print(f"Matches expression: {self.expression}")
            print(f"Executing {self.name}.{self.action}")
            return self.execute()
        else:
            print(f"Does not match expression: {self.expression}")
