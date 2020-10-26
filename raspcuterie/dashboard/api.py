from flask import Blueprint, send_file, jsonify

from raspcuterie import base_path, FAKE_VALUES
from raspcuterie.db import connection
from raspcuterie.devices.relay import OutputDevice

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/am2302/current.json")
def am2303_current():
    """
    Returns the current values for the humidity and temperature
    :return:
    """
    from raspcuterie.devices.am2302 import AM2302

    humidity, temperature = AM2302.read()

    return jsonify(dict(temperature=temperature, humidity=humidity))


@bp.route("/hx711/current.json")
def hx711_current():
    """
    Returns the current values for the humidity and temperature
    :return:
    """
    from raspcuterie.devices.hx711.calibration import hx

    return jsonify(dict(weight=hx.get_grams()))


@bp.route("/hx711/24.json")
def hx711_last_24_hours():
    with connection:
        cursor = connection.execute(
            """SELECT time, value
FROM weight
WHERE time >= date('now', '-3 hours')
ORDER BY time DESC;"""
        )

        data = cursor.fetchall()

        cursor.close()

    return jsonify(data)


@bp.route("/am2302/temperature.json")
def am2303_temperature():
    with connection:
        cursor = connection.execute(
            """SELECT time, value
FROM temperature
WHERE time >= date('now', '-3 hours')
ORDER BY time DESC;""")

        data = cursor.fetchall()
        cursor.close()

    return jsonify(data)


@bp.route("/am2302/humidity.json")
def am2303_humidity():
    with connection:
        cursor = connection.execute(
            """SELECT time, value
FROM humidity
WHERE time >= date('now', '-3 hours')
ORDER BY time DESC;"""
        )

        data = cursor.fetchall()

        cursor.close()

    return jsonify(data)


@bp.route("/am2302/chart.json")
def am2303_chart():
    with connection:
        cursor = connection.execute(
            """SELECT datetime(strftime('%s', t.time) - (strftime('%s', t.time) % (5 * 60)), 'unixepoch') time,
       round(avg(value), 2)                                                                value
FROM temperature t
WHERE t.value is not null
  and time >= datetime('now', '-24 hours')
GROUP BY strftime('%s', t.time) / (5 * 60)
ORDER BY time DESC;"""
        )

        temperature = cursor.fetchall()
        cursor.close()

    with connection:
        cursor = connection.execute(
            """SELECT datetime(strftime('%s', t.time) - (strftime('%s', t.time) % (5 * 60)), 'unixepoch') time,
       round(avg(value), 2)                                                                value
FROM humidity t
WHERE t.value is not null
  and time >= datetime('now', '-24 hours')
GROUP BY strftime('%s', t.time) / (5 * 60)
ORDER BY time DESC;"""
        )

        humidity = cursor.fetchall()

        cursor.close()

    return jsonify(
        [
            dict(data=temperature, name="Temperature"),
            dict(name="Humidity", data=humidity),
        ]
    )


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


@bp.route("/relay/chart.json")
def relay_chart():
    with connection:
        cursor = connection.execute(
            """SELECT time, value_1, value_2, value_3, value_4
FROM relay
WHERE time >= date('now', '-3 hours')
ORDER BY time DESC;"""
        )

        temperature = cursor.fetchall()
        cursor.close()

    return jsonify(
        temperature
    )


@bp.route("/relay/<name>/toggle")
def relay_toggle(name):
    device = OutputDevice.registry[name]

    if device.value == 0:
        device.on()
    else:
        device.off()

    return jsonify(dict(state=device.value))
