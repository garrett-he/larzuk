# larzuk

A command-line tool to help user to modify game data in [Python][1] codes
for [Diablo II: Resurrected][2].

## How to Use

1. Install this command-line tool via `pip`:

    ```shell
    $ pip install larzuk
    ```
2. Write migration scripts in a directory (e.g. `migrations`):

    ```python
    # Relative path of .txt file you want to modify.
    target = 'global/excel/armor.txt'

    # Entry function of migration
    def migrate(txt_file):
        for row in txt_file:
            row['minac'] = row['maxac']
    ```

3. Run `larzuk` command to do migrations:

    ```shell
    $ larzuk up --data-dir /path/to/d2r/data
    ```

4. Check file `armor.txt` in data directory, values in column `minac` equal
   to `maxac`.

## License

Copyright (C) 2023 Garrett HE <garrett.he@hotmail.com>

The GNU General Public License (GPL) version 3, see [LICENSE](./LICENSE).

[1]: https://python.org

[2]: https://diablo2.blizzard.com
