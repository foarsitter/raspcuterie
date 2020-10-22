import sqlite3
from datetime import datetime

from raspcuterie import base_path

db_path = base_path / "raspcuterie.db"

connection = sqlite3.connect(db_path, check_same_thread=False)


def init_db():
    schema_file = base_path / "raspcuterie" / "db" / "schema.sql"

    with schema_file.open() as f:
        connection.cursor().executescript(f.read())

    print("Database Initialized")


def insert_temperature(value: float):
    with connection:
        connection.execute(
            "INSERT INTO temperature(time,value) VALUES (?,?)", (datetime.now(), value)
        )


def insert_humidity(value: float):
    with connection:
        connection.execute(
            "INSERT INTO humidity(time,value) VALUES (?,?)", (datetime.now(), value)
        )


def insert_relay(value_1, value_2, value_3, value_4):
    with connection:
        connection.execute(
            "INSERT INTO relay(time,value_1, value_2, value_3, value_4) VALUES (?, ?, ?, ?, ?)",
            (datetime.now(), value_1, value_2, value_3, value_4),
        )


def insert_weight(value: float):
    with connection:
        connection.execute(
            "INSERT INTO weight(time,value) VALUES (?,?)", (datetime.now(), value)
        )
