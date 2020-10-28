from raspcuterie import db
from raspcuterie.devices import InputDevice


class AM2302(InputDevice):
    type = "AM2303"

    def read(self):
        import Adafruit_DHT # noqa

        sensor = Adafruit_DHT.DHT22

        pin = 4
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin, delay_seconds=0.2)

        return round(humidity, 2), round(temperature, 2)

    def get_context(self):

        humidity, temperature = self.read()

        return dict(humidity=humidity, temperature=temperature)

    def read_from_database(self):
        temperature = db.connection.execute(
            "SELECT value FROM temperature ORDER BY time DESC LIMIT 1"
        ).fetchone()[0]
        humidity = db.connection.execute(
            "SELECT value FROM humidity ORDER BY time DESC LIMIT 1"
        ).fetchone()[0]

        return humidity, temperature

    def temperature_data(self):
        with db.connection:
            cursor = db.connection.execute(
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
            return temperature_data

    def humidity_data(self):
        with db.connection:
            cursor = db.connection.execute(
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

            return humidity_data

    def log(self):
        humidity, temperature = self.read()

        db.insert_humidity(humidity)
        db.insert_temperature(temperature)
