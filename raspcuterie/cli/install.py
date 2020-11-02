import subprocess
from pathlib import Path

import click

from raspcuterie import base_path
from raspcuterie.cli import cli


@cli.group()
def install():
    pass


@install.command()
def systemd():

    input_path = base_path / "raspcuterie.service"

    click.echo(f"sudo cp {input_path} /etc/systemd/system")
    subprocess.call(["sudo", "cp", str(input_path), "/etc/systemd/system"])

    click.echo("sudo systemctl daemon-reload")
    subprocess.call(["sudo", "systemctl", "daemon-reload"])

    click.echo("sudo systemctl enable raspcuterie.service")
    subprocess.call(["sudo", "systemctl", "enable", "raspcuterie.service"])

    click.echo("sudo systemctl start raspcuterie")
    subprocess.call(["sudo", "systemctl", "start", "raspcuterie"])


@install.command()
def cron():

    pi_cron_path = Path("/var/spool/cron/pi")

    if not pi_cron_path.is_dir():
        pi_cron_path.mkdir()

    pi_cron_file = pi_cron_path / "cron"

    with pi_cron_file.open("w") as f:
        f.write("1 * * * * raspcuterie-cli log-values")
