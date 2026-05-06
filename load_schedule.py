"""
Тонкий CLI-обёртка над :mod:`backend.app.utils.import_schedule`.

Автоматически определяет формат файла по расширению (.xlsx / .xls / .pdf)
и вызывает соответствующий парсер.

Примеры использования::

    python load_schedule.py 13.04.2026.xlsx
    python load_schedule.py 13.04.2026.pdf --date 2026-04-13
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.utils.import_schedule import import_schedule


def main():
    parser = argparse.ArgumentParser(
        description="Импорт расписания из Excel (.xlsx/.xls) или PDF (.pdf) в БД."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="13.04.2026.xlsx",
        help="Путь к файлу расписания (по умолчанию 13.04.2026.xlsx)",
    )
    parser.add_argument(
        "--date",
        default="2026-04-13",
        help="Дата расписания в формате YYYY-MM-DD (по умолчанию 2026-04-13)",
    )
    args = parser.parse_args()

    import_schedule(args.file, args.date)


if __name__ == "__main__":
    main()
