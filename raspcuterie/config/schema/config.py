from typing import List, Union, Dict

from pydantic import BaseModel, Field, Extra
from pydantic.fields import Annotated

from .charts import ChartSchema
from .control import ControlGroupSchema
from .devices import (
    AM2302Schema,
    BME280Schema,
    RelaySwitchSchema,
    SinusSchema,
    DBRelaySwitchSchema,
)


DevicesUnion = Annotated[
    Union[
        RelaySwitchSchema,
        DBRelaySwitchSchema,
        AM2302Schema,
        BME280Schema,
        SinusSchema,
    ],
    Field(discriminator="type"),
]


class RaspcuterieConfigSchema(BaseModel):
    name: str
    devices: List[DevicesUnion]

    control: Dict[str, ControlGroupSchema]
    charts: Dict[str, ChartSchema]

    class Config:
        extra = Extra.allow
