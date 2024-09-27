from os import getcwd, PathLike
from pathlib import Path

import click
from larzuk.migrate import discover_migrations, MigrationManager


@click.command('up')
@click.option('--data-dir', help='Path of data directory.', type=click.Path(file_okay=False, exists=True), required=True)
@click.option('--migration-dir', help='Path of migration directory.', type=click.Path(file_okay=False, exists=True), required=False, default=Path(getcwd(), 'migrations'))
def up_command(data_dir: PathLike, migration_dir: PathLike):
    """Apply migrations"""

    mm = MigrationManager(data_dir)

    for migration in discover_migrations(migration_dir):
        mm.apply(migration)
        click.echo(f'[DONE] {migration.name} applied.')
