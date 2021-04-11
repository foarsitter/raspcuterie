import abc
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel


class DegreeSchema(str, Enum):
    celsius = "celsius"
    fahrenheit = "fahrenheit"


class InputDeviceSchema(BaseModel, abc.ABC):
    pass


class OutputDeviceSchema(BaseModel, abc.ABC):
    pass


class AM2302Schema(InputDeviceSchema):
    type: Literal["am2302"]
    degree: Optional[DegreeSchema] = DegreeSchema.celsius
    table_prefix: Optional[str]
    gpio: int


class SinusSchema(InputDeviceSchema):
    type: Literal["sinus"]
    degree: Optional[DegreeSchema]


class BME280Schema(InputDeviceSchema):
    type: Literal["bme280"]


class RelaySwitchSchema(OutputDeviceSchema):
    type: Literal["relay"]
    name: str
    gpio: int
    timeout: Optional[int] = 10
