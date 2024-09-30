from __future__ import annotations
import importlib.util
import sqlite3
from os import PathLike, listdir
from pathlib import Path
from typing import List, Callable
from types import ModuleType
from dataclasses import dataclass

from d2txt import D2TXT
from diff_match_patch import diff_match_patch


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


class MigrationManager:
    target_dir: PathLike
    db: sqlite3.Connection

    def __init__(self, target_dir: PathLike):
        self.target_dir = target_dir

    def connect_db(self):
        db_file = self.target_dir.joinpath('larzuk.sqlite')
        initialized = db_file.exists()

        db = sqlite3.connect(db_file)

        if not initialized:
            sql = 'CREATE TABLE migrations (name TEXT NOT NULL, target TEXT NULL, diff TEXT NULL)'
            db.execute(sql)

        return db

    def apply(self, migration: Migration):
        sql = 'SELECT COUNT(*) FROM migrations WHERE name = ?'
        row = self.db.execute(sql, (migration.name,)).fetchone()

        if row[0] > 0:
            raise MigrationApplyError(migration.name)

        target_path = Path(self.target_dir, migration.module.target)
        origin_text = target_path.read_text(encoding='utf-8')

        txt_file = D2TXT.load_txt(target_path)
        migration.module.migrate(txt_file)
        txt_file.to_txt(target_path)

        modified_text = target_path.read_text(encoding='utf-8')

        dmp = diff_match_patch()
        patches = dmp.patch_make(modified_text, origin_text)

        sql = 'INSERT INTO migrations (name, target, diff) VALUES(?, ?, ?)'
        self.db.execute(sql, (migration.name, migration.module.target, dmp.patch_toText(patches),))
        self.db.commit()


class MigrationApplyError(RuntimeError):
    ...
