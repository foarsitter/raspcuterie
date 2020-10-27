from flask import render_template, Blueprint

from raspcuterie.db import connection
from raspcuterie.devices import OutputDevice, InputDevice

bp = Blueprint("dashboard", __name__)


@bp.route("/")
def dashboard():

    refrigerator = OutputDevice.registry["refrigerator"]
    heater = OutputDevice.registry["heater"]
    dehumidifier = OutputDevice.registry["dehumidifier"]
    humidifier = OutputDevice.registry["humidifier"]

    temperature = connection.execute("SELECT value FROM temperature ORDER BY time DESC LIMIT 1").fetchone()[0]
    humidity = connection.execute("SELECT value FROM humidity ORDER BY time DESC LIMIT 1").fetchone()[0]

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

        temperature_data = cursor.fetchall()
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

        humidity_data = cursor.fetchall()

        cursor.close()

    x = list(dict(temperature_data).values())
    if x:
        temperature_min = min(x)
        temperature_max = max(x)
    else:
        temperature_min = 0
        temperature_max = 0

    y = list(dict(humidity_data).values())
    if y:
        humidity_min = min(y)
        humidity_max = max(y)
    else:
        humidity_min = 0
        humidity_max = 0

    return render_template(
        "base.html",
        refrigerator=refrigerator.value(),
        heater=heater.value(),
        dehumidifier=dehumidifier.value(),
        humidifier=humidifier.value(),

        humidifier_data=humidifier.chart(),
        dehumidifier_data=dehumidifier.chart(),
        refrigerator_data=refrigerator.chart(),
        heater_data=heater.chart(),

        humidity=humidity,
        temperature=temperature,
        temperature_min=temperature_min,
        temperature_max=temperature_max,
        temperature_data=temperature_data,
        humidity_data=humidity_data,

        humidity_min=humidity_min,
        humidity_max=humidity_max,

    )
