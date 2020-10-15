from flask import Blueprint, send_file, jsonify

from raspcuterie import base_path
from raspcuterie.db import connection

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/am2302/current.json")
def am2303_current():
    """
    Returns the current values for the humidity and temperature
    :return:
    """
    from raspcuterie.devices import AM2302
    import Adafruit_DHT

    humidity, temperature = Adafruit_DHT.read_retry(AM2302.sensor, AM2302.pin)

    return jsonify(dict(temperature=temperature, humidity=humidity))


@bp.route("/hx711/current.json")
def hx711_current():
    """
    Returns the current values for the humidity and temperature
    :return:
    """
    from raspcuterie.devices.hx711.calibration import hx

    return jsonify(dict(weight=hx.get_grams()))


@bp.route("/am2302/temperature.json")
def am2303_temperature():
    with connection:
        cursor = connection.execute("SELECT time,value FROM temperature")

        data = cursor.fetchall()
        cursor.close()

    return jsonify(data)


@bp.route("/am2302/humidity.json")
def am2303_humidity():
    with connection:
        cursor = connection.execute("SELECT time,value FROM humidity")

        data = cursor.fetchall()

        cursor.close()

    return jsonify(data)


@bp.route("/am2302/chart.json")
def am2303_chart():
    with connection:
        cursor = connection.execute("SELECT time,value FROM temperature WHERE value is not null")

        temperature = cursor.fetchall()
        cursor.close()

    with connection:
        cursor = connection.execute("SELECT time,value FROM humidity WHERE value is not null")

        humidity = cursor.fetchall()

        cursor.close()

    return jsonify([dict(data=temperature, name="Temperature"), dict(name="Humidity", data=humidity)])


@bp.route("/relay/current.json")
def relay_current():
    from raspcuterie.devices.relay import manager

    return jsonify(
        dict(
            relay_1=manager.is_on(1),
            relay_2=manager.is_on(2),
            relay_3=manager.is_on(3),
            relay_4=manager.is_on(4),
        )
    )


@bp.route("/data/<string:path>.json")
def json_data(path: str):
    path = base_path / f"{path}.json"
    return send_file(path)
