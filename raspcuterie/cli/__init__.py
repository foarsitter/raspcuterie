import os
import time
from pathlib import Path

import click
from flask.cli import with_appcontext  # noqa

import raspcuterie
from ..devices import InputDevice, OutputDevice
from ..gpio import GPIO

os.environ.setdefault("FLASK_APP", "raspcuterie.app")

module_path = Path(__file__).parent


@click.group()
def cli():
    pass


from . import cron, fake, install  # noqa


@cli.command(short_help="Echo the current value of the input and output devices")
@with_appcontext
def devices():
    secure_pin = 24

    GPIO.setup(secure_pin, GPIO.OUT)
    GPIO.output(secure_pin, GPIO.HIGH)

    click.echo(f"Setting {secure_pin} to HIGH to activate the AM2302")

    time.sleep(1)

    click.echo("Listing input devices:")
    click.echo("============================")

    for key, device in InputDevice.registry.items():
        try:
            click.echo(f"{key}: {device.read()}")
        except Exception as e:
            click.echo(click.style(f"{key}: {e}", fg="red"), err=True)

    click.echo("")
    click.echo("Listing output devices:")
    click.echo("============================")

    for key, device in OutputDevice.registry.items():
        try:
            click.echo(f"{key}: {device.value()}")
        except Exception as e:
            click.echo(click.style(f"{key}: {e}", fg="red"), err=True)

    click.echo(f"Setting {secure_pin} to LOW to disable the AM2302")


@cli.command(short_help="Edit the configuration file")
def config():

    file = raspcuterie.base_path / "config.yaml"

    if not raspcuterie.base_path.exists():
        raspcuterie.base_path.mkdir(parents=True)

    if not file.exists():
        x = module_path / "config.yaml"
        with file.open("w") as f:
            f.write(x.read_text())

    click.echo(f"Editing {file} ")
    click.edit(filename=file)


@cli.command(short_help="Version number")
def version():
    click.echo(raspcuterie.version)

    file = raspcuterie.base_path / "config.yaml"

    click.echo(f"Config: {file} ")


@cli.command(short_help="Write schema to raspcuterie.json")
def schema():

    output_file = Path("raspcuterie.schema.json")

    from ..config import RaspcuterieConfigSchema

    RaspcuterieConfigSchema.update_forward_refs()
    output_file.write_text(RaspcuterieConfigSchema.schema_json())
