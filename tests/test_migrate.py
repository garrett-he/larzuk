import importlib.resources
from larzuk.migrate import discover_migrations
from typing import Callable


def test_discover_migrations():
    migrations = discover_migrations(importlib.resources.files('tests.res').joinpath('migrations'))

    assert len(migrations) == 2
    assert migrations[0].name == '01_test1.py'
    assert migrations[0].module.target == '/path/to/txtfile1'
    assert isinstance(migrations[0].module.migrate, Callable)

    assert migrations[1].name == '02_test2.py'
    assert migrations[1].module.target == '/path/to/txtfile2'
    assert isinstance(migrations[1].module.migrate, Callable)
