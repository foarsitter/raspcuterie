from typing import List

from pydantic import BaseModel


class ChartSchema(BaseModel):
    name: str
    series: List[str]
