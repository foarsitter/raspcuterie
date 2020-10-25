from raspcuterie.devices.am2302 import AM2302
from raspcuterie.devices.relay import ReplaySwitch


class ConfigRule:
    def __init__(self, device: ReplaySwitch, expression: str, action: str, name=None):
        self.name = name
        self.device: ReplaySwitch = device
        self.expression: str = expression
        self.action: str = action

    def context(self):

        humidity, temperature = AM2302.read()

        return dict(temperature=temperature, humidity=humidity)

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
