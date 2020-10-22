import click

from raspcuterie.cli import cli
import datetime
import random
from raspcuterie import db


def date_generator(start, stop, **interval):
    while start < stop:
        yield start
        start += datetime.timedelta(**interval)


@cli.group()
def fake():
    pass


@fake.command()
def temperature():
    insert_single_value_data(db.insert_temperature)


@fake.command()
def humidity():
    insert_single_value_data(db.insert_humidity)


@fake.command()
def weight():
    insert_single_value_data(db.insert_weight)




def insert_single_value_data(callable):
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(hours=24)
    x = list(date_generator(yesterday, today, minutes=1))

    with click.progressbar(x) as bar:
        for date in bar:
            callable(random.randint(5, 25), date)