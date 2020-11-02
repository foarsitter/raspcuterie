from flask.cli import FlaskGroup

from raspcuterie.dashboard.app import create_app

cli = FlaskGroup(create_app=create_app)

from . import cron, fake  # noqa
