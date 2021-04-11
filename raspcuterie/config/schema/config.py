from typing import List, Union, Dict

from pydantic import BaseModel, Field

from .control import ControlGroupSchema
from .devices import AM2302Schema, BME280Schema, RelaySwitchSchema, SinusSchema


class RaspcuterieConfigSchema(BaseModel):
    name: str
    devices: List[
        Union[RelaySwitchSchema, AM2302Schema, BME280Schema, SinusSchema]
    ] = Field(..., discriminator="type")

    control: Dict[str, ControlGroupSchema]
