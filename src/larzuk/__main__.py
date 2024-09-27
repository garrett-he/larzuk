import click

from larzuk import __version__
from larzuk.commands import command_group


def print_version(ctx: click.Context, _, value: bool):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


@click.group(commands=command_group)
@click.version_option(message='%(version)s')
def cli():
    """A command-line tool to help user to modify game data in Python codes for Diablo II: Resurrected."""


if __name__ == '__main__':
    cli()
