from flask.cli import FlaskGroup

from raspcuterie.app import create_app


cli = FlaskGroup(create_app=create_app)

from . import cron, fake, test, install  # noqa
