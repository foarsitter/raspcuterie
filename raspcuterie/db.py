import sqlite3
from datetime import datetime

from raspcuterie import base_path

db_path = base_path / "raspcuterie.db"

connection = sqlite3.connect(db_path, check_same_thread=False)


def init_humidity_table():
    with connection:
        connection.execute(
            "create table humidity (id integer primary key, time text not null, value real not null)"
        )


def init_temperature_table():
    with connection:
        connection.execute(
            "create table temperature (id integer primary key, time text not null, value real not null)"
        )


def init_relay_table():
    with connection:
        connection.execute(
            """create table relay
(
    id      int
        constraint relay_pk
            primary key,
    time    text not null,
    value_1 INTEGER default 0,
    value_2 INTEGER default 0,
    value_3 INTEGER default 0,
    value_4 INTEGER default 0
);"""
        )


def init_weight_table():
    with connection:
        connection.execute(
            "create table weight (id integer primary key, time text not null, value real not null)"
        )


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