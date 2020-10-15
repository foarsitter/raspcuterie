import sqlite3
from datetime import datetime

from raspcuterie import base_path

db_path = base_path / "raspcuterie.db"

connection = sqlite3.connect(db_path, check_same_thread=False)


def init_humidity_table():
    with connection:
        connection.execute("create table humidity (id integer primary key, time text not null, value real not null)")


def init_temperature_table():
    with connection:
        connection.execute("create table temperature (id integer primary key, time text not null, value real not null)")


def insert_temperature(value: float):

    with connection:
        connection.execute("INSERT INTO temperature(time,value) VALUES (?,?)", (datetime.now(), value))


def insert_humidity(value: float):

    with connection:
        connection.execute("INSERT INTO humidity(time,value) VALUES (?,?)", (datetime.now(), value))