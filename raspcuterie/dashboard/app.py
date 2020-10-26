from flask import Flask, render_template

from raspcuterie import FAKE_VALUES
from raspcuterie.dashboard import api
from raspcuterie.db import connection
from raspcuterie.devices.hx711 import hx
from raspcuterie.devices.relay import manager
from raspcuterie.devices.am2302 import AM2302

app = Flask(__name__, template_folder="./templates")

app.register_blueprint(api.bp)


@app.route("/")
def dashboard():

    relay_1 = manager.is_on(1)
    relay_2 = manager.is_on(2)
    relay_3 = manager.is_on(3)
    relay_4 = manager.is_on(4)

    temperature = connection.execute("SELECT value FROM temperature ORDER BY time DESC LIMIT 1").fetchone()[0]
    humidity = connection.execute("SELECT value FROM humidity ORDER BY time DESC LIMIT 1").fetchone()[0]

    weight = hx.get_grams()

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

        with connection:
            cursor = connection.execute(
                """SELECT time,value_1
    FROM relay t
    WHERE t.value_1 is not null
      and time >= datetime('now', '-24 hours')
    ORDER BY time DESC;"""
            )

            refrigerator_data = cursor.fetchall()

            cursor.close()
        with connection:
            cursor = connection.execute(
                """SELECT time,value_4
    FROM relay t
    WHERE t.value_2 is not null
      and time >= datetime('now', '-24 hours')
    ORDER BY time DESC;"""
            )

            heater_data = cursor.fetchall()
        with connection:
                cursor = connection.execute(
                    """SELECT time,value_3
        FROM relay t
        WHERE t.value_3 is not null
          and time >= datetime('now', '-24 hours')
        ORDER BY time DESC;"""
                )

                dehumidifier_data = cursor.fetchall()
        with connection:
                cursor = connection.execute(
                        """SELECT time,value_4
            FROM relay t
            WHERE t.value_4 is not null
              and time >= datetime('now', '-24 hours')
            ORDER BY time DESC;"""
                    )

                humidifier_data = cursor.fetchall()

                cursor.close()

    x = list(dict(temperature_data).values())
    temperature_min = min(x)
    temperature_max = max(x)

    y = list(dict(humidity_data).values())
    humidity_min = min(y)
    humidity_max = max(y)

    return render_template(
        "base.html",
        relay_1=relay_1,
        relay_2=relay_2,
        relay_3=relay_3,
        relay_4=relay_4,
        humidity=humidity,
        temperature=temperature,
        temperature_min=temperature_min,
        temperature_max=temperature_max,
        temperature_data=temperature_data,
        humidity_data=humidity_data,
        humidifier_data=humidifier_data,
        dehumidifier_data=dehumidifier_data,
        humidity_min=humidity_min,
        humidity_max=humidity_max,
        refrigerator_data=refrigerator_data,
        heater_data=heater_data,
        weight=weight
    )
