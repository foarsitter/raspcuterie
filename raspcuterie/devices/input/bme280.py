import bme280
from flask import current_app, g
from smbus2 import smbus2

from raspcuterie.db import get_db, insert_temperature, insert_humidity
from raspcuterie.devices import InputDevice, LogDevice, DatabaseDevice


class BME280(InputDevice, LogDevice, DatabaseDevice):
    type = "BME280"

    DEGREE_CELSIUS = "celsius"
    DEGREE_FAHRENHEIT = "fahrenheit"

    table_sql = """
        create table if not exists {0}
        (
            id    integer primary key,
            time  text not null,
            value integer not null
        );"""

    def __init__(self, name, degree=DEGREE_CELSIUS, table_prefix=""):
        super().__init__(name)
        self.port = 1
        self.address = 0x76
        self.degree = degree
        self.table_prefix = table_prefix

    def read(self):
        humidity, temperature = self.raw()

        if humidity:
            humidity = round(humidity, 1)

        if temperature:
            temperature = round(temperature, 1)

        return humidity, temperature

    def get_table_name(self, name):
        return f"{self.table_prefix}{name}"

    @property
    def table_humidity(self):
        return self.get_table_name("humidity")

    @property
    def table_temperature(self):
        return self.get_table_name("temperature")

    def create_table(self, connection):
        connection.execute(BME280.table_sql.format(self.table_humidity))
        connection.execute(BME280.table_sql.format(self.table_temperature))

    def raw(self):
        port = 1
        address = 0x76
        bus = smbus2.SMBus(port)

        calibration_params = bme280.load_calibration_params(bus, address)

        # the sample method will take a single reading and return a
        # compensated_reading object
        sensor = bme280.sample(bus, address, calibration_params)

        # the compensated_reading class has the following attributes

        print(sensor.temperature)

        print(sensor.humidity)

        try:
            temperature = sensor.temperature
            humidity = sensor.humidity
        except RuntimeError as e:
            current_app.logger.error(e)
            temperature = None
            humidity = None

        if self.degree != "celsius" and temperature:
            temperature = temperature * 9 / 5 + 32

        return humidity, temperature

    def get_context(self):
        from raspcuterie.dashboard.api import min_max_avg_over_period

        humidity, temperature = self.read()

        temperature_min, temperature_max, temperature_avg = min_max_avg_over_period(
            self.table_temperature
        )

        humidity_min, humidity_max, humidity_avg = min_max_avg_over_period(
            self.table_humidity
        )

        humidity_min_3h, humidity_max_3h, humidity_avg_3h = min_max_avg_over_period(
            self.table_humidity, "-3 hours"
        )

        values = dict(
            humidity=humidity,
            temperature=temperature,
            temperature_min=temperature_min,
            temperature_max=temperature_max,
            temperature_avg=temperature_avg,
            humidity_min=humidity_min,
            humidity_max=humidity_max,
            humidity_avg=humidity_avg,
            humidity_min_3h=humidity_min_3h,
            humidity_max_3h=humidity_max_3h,
            humidity_avg_3h=humidity_avg_3h,
        )

        values[self.table_temperature] = temperature
        values[self.table_humidity] = humidity

        return values

    def read_from_database(self):

        time = None

        table_name = self.table_temperature

        temperature = (
            get_db()
            .execute(f"SELECT value, time FROM {table_name} ORDER BY time DESC LIMIT 1")
            .fetchone()
        )

        if temperature:
            time = temperature[1]
            temperature = temperature[0]

        table_name = self.table_temperature

        humidity = (
            get_db()
            .execute(f"SELECT value, time FROM {table_name} ORDER BY time DESC LIMIT 1")
            .fetchone()
        )

        if humidity:
            time = humidity[1]
            humidity = humidity[0]

        return humidity, temperature, time

    def temperature_data(self, period="-24 hours", aggregate=5 * 60):

        table_name = self.table_temperature

        cursor = get_db().execute(
            f"""SELECT datetime(strftime('%s', t.time) - (strftime('%s', t.time) % :aggregate), 'unixepoch') time,
       round(avg(value), 2)                                                                value
FROM {table_name} t
WHERE t.value is not null
  and time >= datetime('now', :period)
GROUP BY strftime('%s', t.time) / :aggregate
ORDER BY time DESC;""",
            dict(period=period, aggregate=aggregate),
        )

        temperature_data = cursor.fetchall()
        cursor.close()
        return temperature_data

    def humidity_data(self, period="-24 hours", aggregate=5 * 60):

        table_name = self.table_humidity

        cursor = get_db().execute(
            f"""SELECT datetime(strftime('%s', t.time) - (strftime('%s', t.time) % :aggregate), 'unixepoch') time,
       round(avg(value), 2)                                                                value
FROM {table_name} t
WHERE t.value is not null
  and time >= datetime('now', :period)
GROUP BY strftime('%s', t.time) / :aggregate
ORDER BY time DESC;""",
            dict(period=period, aggregate=aggregate),
        )

        humidity_data = cursor.fetchall()

        cursor.close()

        return humidity_data

    def log(self):
        humidity, temperature = self.read()

        if humidity:
            insert_humidity(humidity, self.table_humidity)
        if temperature:
            insert_temperature(temperature, self.table_temperature)
