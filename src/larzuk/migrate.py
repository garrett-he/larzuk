from __future__ import annotations
import importlib.util
from os import PathLike, listdir
from pathlib import Path
from typing import List, Callable
from types import ModuleType
from dataclasses import dataclass


def discover_migrations(base_dir: PathLike) -> List[Migration]:
    migrations = []

    for filename in filter(lambda f: f[-3:] == '.py', listdir(base_dir)):
        spec = importlib.util.spec_from_file_location(filename, Path(base_dir, filename))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        migrations.append(Migration(name=filename, module=module))

    return migrations


class MigrationModule(ModuleType):
    target: str
    migrate: Callable


@dataclass
class Migration:
    name: str
    module: MigrationModule
