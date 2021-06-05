from flask import Blueprint, current_app, jsonify, request
from werkzeug.exceptions import NotFound

from raspcuterie.config import RaspcuterieConfigSchema
from raspcuterie.devices import InputDevice
from raspcuterie.devices.input.am2302 import AM2302
from raspcuterie.devices.output.relay import OutputDevice, RelaySwitch
from raspcuterie.devices.series import Series
from raspcuterie.utils import gettext

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

    config: RaspcuterieConfigSchema = current_app.schema

    chart = config.charts[chart_name]

    result = []

    for series_name in chart.series:

        series = Series.registry.get(series_name, None)
        if series:
            result.append(dict(name=series.name, data=series.data(period, aggregate)))

    return jsonify(result)


@bp.route("/devices/<device_name>/current.json")
def am2303_current(device_name):
    """
    Returns the current values for the humidity and temperature
    :return:
    """

    from raspcuterie.devices import InputDevice
    from raspcuterie.devices.input import AM2302, BME280

    period = request.args.get("period", "-24 hours")

    device = InputDevice.registry[device_name]

    if isinstance(device, (AM2302, BME280)):

        time, humidity = device.h_series.last_observation(period)
        time, temperature = device.t_series.last_observation(period)

        # temperature_slope = slope(device.t_series.name)
        # humidity_slope = slope(device.h_series.name)
        #
        # temperature_min_max = min_max_avg_over_period(device.t_series.name, period)
        # humidity_min_max = min_max_avg_over_period(device.h_series.name, period)
        #
        # temperature = dict(
        #     current=temperature,
        #     min=round(temperature_min_max[0], 2),
        #     max=round(temperature_min_max[1], 2),
        #     avg=round(temperature_min_max[2], 2),
        #     slope=temperature_slope,
        # )
        #
        # humidity = dict(
        #     current=humidity,
        #     min=humidity_min_max[0],
        #     max=humidity_min_max[1],
        #     avg=round(humidity_min_max[2], 2),
        #     slope=humidity_slope,
        # )

        return jsonify(
            dict(
                temperature=temperature,
                humidity=humidity,
                time=time[: len("2020-12-22 11:08:10")] if time else None,
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
