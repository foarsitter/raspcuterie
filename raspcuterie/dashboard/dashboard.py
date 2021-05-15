from typing import Dict

from flask import Blueprint, current_app, render_template
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers.data import YamlLexer

from raspcuterie.config import RaspcuterieConfigSchema
from raspcuterie.dashboard.apexcharts import ChartObject, YAxis
from raspcuterie.devices import OutputDevice
from raspcuterie.devices.series import Series

bp = Blueprint("dashboard", __name__, template_folder="./templates")


@bp.route("/")
def dashboard():

    config = current_app.config["config"]
    formatter = HtmlFormatter(linenos=True, style="friendly", noclasses=True)
    config_text = highlight(config, YamlLexer(), formatter)

    charts_json: Dict[str, str] = {}

    s: RaspcuterieConfigSchema = current_app.schema

    for name, schema in s.charts.items():
        obj = ChartObject()
        obj.title.text = schema.title
        obj.chart.id = name

        for series in schema.series:
            series_obj = Series.registry.get(series, None)

            if series_obj is None:
                raise Exception(f"{series} does not exists")

            if series_obj.type == "boolean":
                obj.stroke.curve.append("stepline")
                obj.markers.size.append(2)
                obj.yaxis.append(
                    YAxis(
                        tickAmount=1,
                        opposite=True,
                        show=False,
                        min=0,
                        max=3,
                        serieName=series,
                    )
                )
            elif series_obj.type == "integer":
                obj.markers.size.append(0)
                obj.yaxis.append(
                    YAxis(
                        tickAmount=4,
                        opposite=False,
                        show=True,
                        min=0,
                        max=100,
                        serieName=series,
                    )
                )
                obj.stroke.curve.append("smooth")

        charts_json[name] = obj.json()

    return render_template(
        "dashboard.html",
        config_text=config_text,
        output_devices=OutputDevice.registry,
        charts=current_app.schema.charts,
        charts_json=charts_json,
    )
