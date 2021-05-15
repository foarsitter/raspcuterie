from typing import List

from pydantic import BaseModel


class Chart(BaseModel):
    id: str
    type: str
    group: str
    height: int
    width = "100%"


class Title(BaseModel):
    text: str
    align: str


class Stroke(BaseModel):
    curve: List[str]
    width: int


class Markers(BaseModel):
    size: List[int]


class Label(BaseModel):
    minWidth: int = 40


class YAxis(BaseModel):
    tickAmount: int
    serieName: str
    min: int
    max: int
    opposite: bool
    show: bool
    # labels: Label = Label(minWidth=40)


class DatetimeFormatter(BaseModel):
    year: str = "yyyy"
    month: str = "MMM 'yy"
    day: str = "dd MMM"
    hour: str = "HH:mm"


class XLabels(BaseModel):
    datetimeFormatter: DatetimeFormatter = DatetimeFormatter()
    datetimeUTC: bool = False


class XAxis(BaseModel):
    type: str = "datetime"
    labels: XLabels = XLabels()


class XToolTip(BaseModel):
    show: bool = True
    format: str = "HH:mm"


class Tooltip(BaseModel):
    x: XToolTip = XToolTip()


class ChartObject(BaseModel):
    chart: Chart = Chart(id="", type="line", group="social", height=230)
    title: Title = Title(text="", align="left")
    stroke: Stroke = Stroke(curve=[], width=1)
    markers: Markers = Markers(size=[])
    tooltip: Tooltip = Tooltip()
    xaxis: XAxis = XAxis()
    yaxis: List[YAxis] = []
