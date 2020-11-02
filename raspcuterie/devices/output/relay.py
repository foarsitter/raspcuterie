import datetime
from builtins import super

from raspcuterie.db import get_db
from raspcuterie.devices import OutputDevice, DatabaseDevice, LogDevice
from raspcuterie.gpio import GPIO


class RelaySwitch(OutputDevice, DatabaseDevice, LogDevice):
    type = "relay"

    table_sql = """
    create table if not exists {0}
    (
        id    integer primary key,
        time  text not null,
        value integer not null
    );"""

    def __init__(self, name, gpio):
        super(RelaySwitch, self).__init__(name)

        self.last_witch = datetime.datetime.now() - datetime.timedelta(seconds=60)

        self.pin_number = gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_number, GPIO.OUT)

    def create_table(self, connection):
        connection.execute(RelaySwitch.table_sql.format(self.table_name))

    def on(self):
        if True or self.last_witch < datetime.datetime.now() - datetime.timedelta(
                seconds=60
        ):
            GPIO.output(self.pin_number, GPIO.HIGH)
            self.last_witch = datetime.datetime.now()
        else:
            print("timeout")
        self.update_table(self.value())

    def off(self):
        GPIO.output(self.pin_number, GPIO.LOW)

        self.update_table(self.value())

    def value(self):
        return GPIO.input(self.pin_number)

    def chart(self):
        cursor = get_db().execute(
            """SELECT time,value
FROM {0} t
WHERE t.value is not null
  and time >= datetime('now', '-24 hours')
ORDER BY time DESC;""".format(
                self.table_name
            )
        )

        return cursor.fetchall()

    def update_table(self, value):

        db = get_db()

        with db:
            db.execute(
                "INSERT INTO {0}(time,value) VALUES (?,?)".format(self.table_name),
                (datetime.datetime.now(), value),
            )

    @property
    def table_name(self):
        return "relay_" + self.name


class DBRelay(RelaySwitch, DatabaseDevice, LogDevice):
    type = "dbrelay"

    def __init__(self, name, **kwargs):
        super(RelaySwitch, self).__init__(name)

    @property
    def table_name(self):
        return "dbrelay_" + self.name

    def on(self):
        self.update_table(True)

    def off(self):
        self.update_table(False)

    def value(self):
        cursor = get_db().execute(
            "SELECT value FROM {0} ORDER BY time DESC LIMIT 1".format(self.table_name)
        )

        row = cursor.fetchone()

        if row:
            return bool(row[0])
