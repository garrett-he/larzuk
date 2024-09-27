import os
import tempfile
import shutil
import hashlib
import importlib.resources
from pathlib import Path
from larzuk.migrate import discover_migrations, MigrationManager
from typing import Callable


def test_discover_migrations():
    migrations = discover_migrations(importlib.resources.files('tests.res').joinpath('migrations'))

    assert len(migrations) == 1
    assert migrations[0].name == '01_test1.py'
    assert migrations[0].module.target == 'armor.txt'
    assert isinstance(migrations[0].module.migrate, Callable)


def test_migration_manager():
    data_dir = importlib.resources.files('tests.res').joinpath('data')
    armor_txt = Path(tempfile.gettempdir(), 'armor.txt')
    shutil.copy(data_dir.joinpath('armor.txt'), armor_txt)

    mm = MigrationManager(tempfile.gettempdir())

    for migration in discover_migrations(importlib.resources.files('tests.res').joinpath('migrations')):
        mm.apply(migration)

    assert hashlib.md5(open(armor_txt, 'rb').read()).hexdigest() == '4a978e67e270c8a41ba935e14247554b'
    os.unlink(armor_txt)
