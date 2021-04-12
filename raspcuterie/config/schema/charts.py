from typing import List

from pydantic import BaseModel


class ChartSchema(BaseModel):
    title: str
    series: List[str]
