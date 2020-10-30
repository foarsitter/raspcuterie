from abc import abstractmethod, ABC
from typing import Dict, Type


class InputDevice(ABC):
    type: str
    registry: Dict[str, "InputDevice"] = {}
    types: Dict[str, Type["InputDevice"]] = {}

    def __init__(self, name):
        InputDevice.registry[name] = self
        self.name = name

    def __init_subclass__(cls, **kwargs):
        super(InputDevice, cls).__init_subclass__(**kwargs)

        if hasattr(cls, "type") and cls.type:
            name = cls.type
        else:
            name = cls.__name__

        InputDevice.types[name] = cls

    @abstractmethod
    def read(self):
        raise NotImplementedError

    def get_context(self):
        return {}

    def log(self):
        return


class OutputDevice(ABC):
    type: str
    registry: Dict[str, "OutputDevice"] = {}
    types: Dict[str, Type["OutputDevice"]] = {}

    def __init__(self, name):
        OutputDevice.registry[name] = self
        self.name = name

    def __init_subclass__(cls, **kwargs):
        super(OutputDevice, cls).__init_subclass__(**kwargs)
        OutputDevice.types[cls.type] = cls

    @abstractmethod
    def value(self):
        raise NotImplementedError

    def get_context(self):
        return {self.name: self.value()}

    def log(self):
        return
