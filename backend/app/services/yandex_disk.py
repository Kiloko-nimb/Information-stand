"""
Синхронизация расписания с публичной папки Яндекс.Диска.

В ККРИТ PDF/Excel с расписанием выкладываются на Яндекс.Диск в публичную
папку. Этот модуль умеет:

1. Получить список файлов в публичной папке (без OAuth-токена — достаточно
   публичной ссылки на папку).
2. Извлечь дату из имени файла (например, "13.04.2026.pdf" → 2026-04-13).
3. Скачать файл локально.
4. Импортировать его в БД через ``import_schedule``.

Публичный API Яндекс.Диска: https://yandex.ru/dev/disk-api/doc/ru/reference/public
"""
from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

import requests

logger = logging.getLogger(__name__)

_PUBLIC_API = "https://cloud-api.yandex.net/v1/disk/public/resources"
_DOWNLOAD_API = "https://cloud-api.yandex.net/v1/disk/public/resources/download"

# Типичные разделители в имени файла: 13.04.2026, 13-04-2026, 13_04_2026.
_DATE_RE = re.compile(r"(\d{1,2})[._-](\d{1,2})[._-](\d{4})")

_SUPPORTED_EXTS = {".xlsx", ".xls", ".pdf"}


@dataclass
class YandexFile:
    name: str
    path: str  # путь внутри публичной папки ("/" или "/subfolder/file.pdf")
    size: int
    modified: datetime
    parsed_date: Optional[date]

    @property
    def extension(self) -> str:
        return Path(self.name).suffix.lower()


def parse_date_from_filename(name: str) -> Optional[date]:
    """Извлечь дату вида '13.04.2026' / '13-04-2026' / '13_04_2026'."""
    m = _DATE_RE.search(name)
    if not m:
        return None
    try:
        d, mo, y = (int(x) for x in m.groups())
        return date(y, mo, d)
    except ValueError:
        return None


def list_public_folder(
    public_url: str,
    *,
    session: Optional[requests.Session] = None,
    limit: int = 200,
) -> List[YandexFile]:
    """Получить список файлов из публичной папки Яндекс.Диска."""
    sess = session or requests.Session()
    resp = sess.get(
        _PUBLIC_API,
        params={"public_key": public_url, "limit": limit},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    items = data.get("_embedded", {}).get("items", [])
    result: List[YandexFile] = []
    for item in items:
        if item.get("type") != "file":
            continue
        name = item.get("name", "")
        if Path(name).suffix.lower() not in _SUPPORTED_EXTS:
            continue
        try:
            modified = datetime.fromisoformat(
                item.get("modified", "").replace("Z", "+00:00")
            )
        except ValueError:
            modified = datetime.utcnow()
        result.append(
            YandexFile(
                name=name,
                path=item.get("path", "/"),
                size=item.get("size", 0),
                modified=modified,
                parsed_date=parse_date_from_filename(name),
            )
        )
    return result


def download_file(
    public_url: str,
    file_path: str,
    destination: Path,
    *,
    session: Optional[requests.Session] = None,
) -> Path:
    """Скачать файл из публичной папки по внутреннему пути."""
    sess = session or requests.Session()
    resp = sess.get(
        _DOWNLOAD_API,
        params={"public_key": public_url, "path": file_path},
        timeout=15,
    )
    resp.raise_for_status()
    href = resp.json().get("href")
    if not href:
        raise RuntimeError(
            f"Ответ Яндекс.Диска не содержит ссылки на скачивание: {resp.json()}"
        )

    dl = sess.get(href, stream=True, timeout=60)
    dl.raise_for_status()
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as f:
        for chunk in dl.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return destination


def sync_folder(
    public_url: str,
    download_dir: Path,
    *,
    session: Optional[requests.Session] = None,
) -> List[tuple[YandexFile, Path]]:
    """
    Скачать все файлы с распознанной датой из публичной папки.

    Возвращает список ``(YandexFile, local_path)`` — уже скачанных и
    пригодных для импорта. Уже существующие файлы не перекачиваются
    (проверка по имени и размеру).
    """
    sess = session or requests.Session()
    files = list_public_folder(public_url, session=sess)
    results: List[tuple[YandexFile, Path]] = []
    for f in files:
        if f.parsed_date is None:
            logger.info(
                "Пропускаем %s: не удалось распознать дату в имени файла", f.name
            )
            continue
        local = download_dir / f.name
        if local.exists() and local.stat().st_size == f.size and f.size > 0:
            logger.info("Файл %s уже скачан, пропускаем", f.name)
        else:
            logger.info("Скачиваем %s (%d bytes)", f.name, f.size)
            download_file(public_url, f.path, local, session=sess)
        results.append((f, local))
    return results


def sync_and_import(
    public_url: str,
    download_dir: Path,
) -> List[tuple[date, Path, int]]:
    """
    Скачать и импортировать все расписания из публичной папки.

    Возвращает ``[(date, local_path, records_added), ...]``.
    Ошибки импорта не прерывают пайплайн — они логируются, и процесс
    продолжает работу с остальными файлами.
    """
    from app.utils.import_schedule import import_schedule

    summary: List[tuple[date, Path, int]] = []
    for f, local in sync_folder(public_url, download_dir):
        try:
            added = import_schedule(
                str(local), f.parsed_date.strftime("%Y-%m-%d")
            )
            summary.append((f.parsed_date, local, added or 0))
        except Exception as exc:
            logger.error(
                "Ошибка импорта %s (%s): %s", f.name, f.parsed_date, exc
            )
    return summary


def _main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Синхронизация расписания ККРИТ с Яндекс.Диска."
    )
    parser.add_argument(
        "--url",
        default=os.environ.get("YANDEX_DISK_PUBLIC_URL"),
        help="Публичная ссылка на папку (или env YANDEX_DISK_PUBLIC_URL).",
    )
    parser.add_argument(
        "--dest",
        default="data/schedule-downloads",
        help="Куда сохранять скачанные файлы (по умолчанию data/schedule-downloads).",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="Только показать список файлов, ничего не скачивать.",
    )
    args = parser.parse_args()

    if not args.url:
        parser.error(
            "Требуется публичная ссылка на папку (--url или переменная окружения "
            "YANDEX_DISK_PUBLIC_URL)."
        )

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if args.list_only:
        for f in list_public_folder(args.url):
            print(f"{f.parsed_date or '??':10}  {f.size:>10}  {f.name}")
        return

    dest = Path(args.dest)
    summary = sync_and_import(args.url, dest)
    print(f"Готово. Обработано файлов: {len(summary)}")
    for day, path, added in summary:
        print(f"  {day.isoformat()}  {path.name}  +{added} записей")


if __name__ == "__main__":
    _main()
