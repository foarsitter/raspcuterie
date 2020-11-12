import os
import subprocess
from pathlib import Path
from typing import List

import click
from jinja2 import Template

from raspcuterie import base_path
from raspcuterie.cli import cli

module_path = Path(__file__).parent


systemd_template = """
[Unit]
Description=Raspcuterie dashboard
After=network.target

[Service]
User={{user}}
Environment=FLASK_APP=raspcuterie.app
Environment=FLASK_ENV=production
ExecStart={{flask}} run --host 0.0.0.0 --port {{port}}
Restart=always

[Install]
WantedBy=multi-user.target
"""


def read_return(commands: List[str]):

    x = subprocess.Popen(commands, stdout=subprocess.PIPE)
    exec_path, _ = x.communicate()

    exec_path = exec_path.decode("utf-8").replace("\n", "")

    return exec_path


def which(process):
    return read_return(["which", process])


def whoami():
    return read_return(["whoami"])


@cli.group()
def install():
    pass


@install.command()
@click.option("-p", "--port", default="5000")
def systemd(port):

    template = Template(systemd_template)

    systemd_content = template.render(user=whoami(), flask=which("flask"), port=port)

    commands = [
        f'echo "{systemd_content}" | sudo tee /etc/systemd/system/raspcuterie.service',
        "sudo systemctl daemon-reload",
        "sudo systemctl enable raspcuterie.service",
        "sudo systemctl start raspcuterie",
    ]

    for command in commands:
        click.echo(command)
        print(subprocess.call(command, shell=True))


@install.command()
def cron():

    which_raspcuterie = which("raspcuterie")

    command = f"* * * * * {which_raspcuterie} log-values"

    cron_in = subprocess.Popen(["crontab", "-l"], stdout=subprocess.PIPE)
    cur_crontab, _ = cron_in.communicate()

    cur_crontab = cur_crontab.decode("utf-8")

    if command not in cur_crontab:
        click.echo("Updating cronjob")
        cur_crontab += "# raspcuterie every minute"
        cur_crontab += os.linesep
        cur_crontab += command
        cur_crontab += os.linesep
    else:
        click.echo("Command already present")

    cron_out = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE)
    cron_out.communicate(input=cur_crontab.encode("utf-8"))


@cli.command()
def config():

    file = base_path / "config.yaml"

    if not base_path.exists():
        base_path.mkdir(parents=True)

    if not file.exists():
        x = module_path / "config.yaml"
        with file.open("w") as f:
            f.write(x.read_text())

    click.edit(filename=file)
