import pathlib
import click

base_path = pathlib.Path(click.get_app_dir("raspcuterie"))

version = "0.2.0"

lib_path = pathlib.Path(__file__).parent.parent
