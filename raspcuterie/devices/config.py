from gpiozero import LED

from raspcuterie.devices.am2302 import AM2302


class ConfigRule:
    def __init__(self, device: LED, expression: str, action: str):
        self.device: LED = device
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
