import os

import click

from flask.cli import with_appcontext  # noqa

os.environ.setdefault("FLASK_APP", "raspcuterie.app")


@click.group()
def cli():
    pass


from . import cron, fake, test, install  # noqa
