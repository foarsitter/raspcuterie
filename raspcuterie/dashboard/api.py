from typing import List

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

from raspcuterie.devices import InputDevice
from raspcuterie.devices.input.am2302 import AM2302
from raspcuterie.devices.output.relay import OutputDevice, RelaySwitch
from raspcuterie.devices.series import Series
from raspcuterie.utils import gettext, slope, min_max_avg_over_period

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("<series>/current.json")
def current(series: str):

    series = Series.registry.get(series, None)

    if series is None:
        raise NotFound

    return series.last_observation()


@bp.route("chart/<chart_name>/series.json")
def chart_series(chart_name: str):

    period = request.args.get("period", "-24 hours")

    aggregate = request.args.get("aggregate", 5 * 60)

    from raspcuterie.app import get_config

    config = get_config()

    chart = config.charts[chart_name]

    result = []

    for series_name in chart.series:

        series = Series.registry.get(series_name, None)
        if series:
            result.append(dict(name=chart.title, data=series.data(period, aggregate)))

    return result


@bp.route("/am2302/current.json")
def am2303_current():
    """
    Returns the current values for the humidity and temperature
    :return:
    """

    from raspcuterie.devices import InputDevice

    humidity, temperature, time = InputDevice.registry[
        "temperature"
    ].read_from_database()

    temperature_slope = slope("temperature")
    humidity_slope = slope("humidity")

    period = request.args.get("period", "-24 hours")

    temperature_min_max = min_max_avg_over_period("temperature", period)
    humidity_min_max = min_max_avg_over_period("humidity", period)

    temperature = dict(
        current=temperature,
        min=round(temperature_min_max[0], 2),
        max=round(temperature_min_max[1], 2),
        avg=round(temperature_min_max[2], 2),
        slope=temperature_slope,
    )

    humidity = dict(
        current=humidity,
        min=humidity_min_max[0],
        max=humidity_min_max[1],
        avg=round(humidity_min_max[2], 2),
        slope=humidity_slope,
    )

    return jsonify(
        dict(
            temperature=temperature,
            humidity=humidity,
            time=time[: len("2020-12-22 11:08:10")],
        )
    )


@bp.route("/am2302/chart.json")
def am2303_chart():
    am2302: AM2302 = InputDevice.registry["temperature"]

    refrigerator: RelaySwitch = OutputDevice.registry["refrigerator"]
    heater: RelaySwitch = OutputDevice.registry["heater"]

    humidifier: RelaySwitch = OutputDevice.registry["humidifier"]
    dehumidifier: RelaySwitch = OutputDevice.registry["dehumidifier"]

    period = request.args.get("period", "-24 hours")
    aggregate = request.args.get("aggregate", 5 * 60)

    return jsonify(
        dict(
            temperature=[
                dict(
                    name=gettext("Temperature"),
                    data=am2302.temperature_data(period, aggregate),
                ),
                dict(name=gettext("Refrigerator"), data=refrigerator.chart(period)),
                dict(name=gettext("Heater"), data=heater.chart(period)),
            ],
            humidity=[
                dict(
                    data=am2302.humidity_data(period, aggregate),
                    name=gettext("Humidity"),
                ),
                dict(data=humidifier.chart(period), name=gettext("Humidifier")),
                dict(data=dehumidifier.chart(period), name=gettext("Dehumidifier")),
            ],
        )
    )


@bp.route("/relay/current.json")
def relay_current():
    from raspcuterie.devices import OutputDevice

    data = {}

    for key, device in OutputDevice.registry.items():
        if isinstance(device, RelaySwitch):
            data[key] = device.value()

    return jsonify(data)


@bp.route("/relay/<name>/toggle", methods=["POST", "GET"])
def relay_toggle(name):
    device = OutputDevice.registry[name]

    if device.value() == 0:
        device.on()
    else:
        device.off()

    return jsonify(dict(state=device.value()))
