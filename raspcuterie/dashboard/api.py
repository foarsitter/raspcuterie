from flask import Blueprint, jsonify, request
from flask_babel import gettext

from raspcuterie.devices import InputDevice
from raspcuterie.devices.input.am2302 import AM2302
from raspcuterie.devices.output.relay import OutputDevice, RelaySwitch

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/am2302/current.json")
def am2303_current():
    """
    Returns the current values for the humidity and temperature
    :return:
    """
    from raspcuterie.devices import InputDevice

    humidity, temperature, time = InputDevice.registry["temperature"].read_from_database()

    return jsonify(
        dict(
            temperature=temperature,
            humidity=humidity,
            datetime=time,
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
    aggregate = request.args.get("aggregate", 5*60)

    return jsonify(
        dict(
            temperature=[
                dict(name=gettext("Temperature"), data=am2302.temperature_data(period, aggregate)),
                dict(name=gettext("Refrigerator"), data=refrigerator.chart(period)),
                dict(name=gettext("Heater"), data=heater.chart(period)),
            ],
            humidity=[
                dict(data=am2302.humidity_data(period, aggregate), name=gettext("Humidity")),
                dict(data=humidifier.chart(), name=gettext("Humidifier")),
                dict(data=dehumidifier.chart(), name=gettext("Dehumidifier")),
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
