import click


@click.group()
def cli():
    pass


from raspcuterie.scripts import cron  # noqa
