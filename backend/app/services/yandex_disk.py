"""
Синхронизация расписания с публичной папки Яндекс.Диска.

В ККРИТ PDF/Excel с расписанием выкладываются на Яндекс.Диск в публичную
папку. Этот модуль умеет:

1. Получить список файлов в публичной папке (без OAuth-токена — достаточно
   публичной ссылки на папку).
2. Извлечь дату из имени файла (например, "13.04.2026.pdf" → 2026-04-13).
3. Скачать файл локально.
4. Импортировать его в БД через ``import_schedule``.

Чтобы не перепарсить 200 PDF на каждом старте бэкенда, успешно
импортированные файлы запоминаются в манифесте ``.imported.json``
рядом с директорией скачивания (см. ``_load_manifest`` ниже). При
следующем запуске файл с тем же размером и временем модификации,
что уже есть в манифесте, пропускается.

Публичный API Яндекс.Диска: https://yandex.ru/dev/disk-api/doc/ru/reference/public
"""
from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import unquote, urlparse, urlunparse

import requests
from app.utils.retry import RetryableSession

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


def split_public_url(public_url: str) -> Tuple[str, str]:
    """
    Разобрать публичную ссылку Яндекс.Диска на корневой public_key и
    внутренний путь.

    Публичные ссылки бывают двух видов:

    - ``https://disk.yandex.ru/d/<token>`` — ссылка на корень публичной
      папки. Внутренний путь в этом случае ``"/"``.
    - ``https://disk.yandex.ru/d/<token>/<subfolder>/<file>`` — ссылка
      на подпапку/файл внутри публичной папки. API Яндекс.Диска не
      умеет принимать такую ссылку напрямую (вернёт 404), поэтому надо
      разделить её на корневой ``public_key`` и ``path``.

    Возвращает ``(public_key, path)``. ``path`` всегда начинается с ``/``.
    """
    parsed = urlparse(public_url)
    # Путь первой публичной папки всегда вида "/d/<token>[/...]".
    parts = parsed.path.split("/", 3)
    # parts = ['', 'd', '<token>', '<rest>']
    if len(parts) < 3 or parts[1] != "d":
        return public_url, "/"
    root_path = f"/{parts[1]}/{parts[2]}"
    root_url = urlunparse(
        (parsed.scheme, parsed.netloc, root_path, "", "", "")
    )
    inner = f"/{parts[3]}" if len(parts) == 4 and parts[3] else "/"
    return root_url, unquote(inner)


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
    session: Optional[Union[requests.Session, RetryableSession]] = None,
    limit: int = 200,
    recursive: bool = False,
) -> List[YandexFile]:
    """Получить список файлов из публичной папки Яндекс.Диска.

    ``public_url`` может указывать как на корень публичной папки, так и
    на вложенный подкаталог — URL автоматически разобьётся на корень +
    внутренний путь.

    Если ``recursive=True``, обойдёт все вложенные папки. По умолчанию
    берутся файлы только из указанной папки.
    """
    # Используем RetryableSession для автоматического retry при ошибках
    sess = session or RetryableSession()
    close_session = session is None
    public_key, inner_path = split_public_url(public_url)

    result: List[YandexFile] = []
    to_visit: List[str] = [inner_path]
    seen: set[str] = set()

    while to_visit:
        current = to_visit.pop(0)
        if current in seen:
            continue
        seen.add(current)

        # Yandex API отдаёт результаты постранично (limit + offset). Если
        # в папке больше `limit` файлов — без явного цикла часть просто
        # потеряется. У ККРИТ в публичной папке уже >200 PDF, поэтому
        # пагинация обязательна.
        offset = 0
        while True:
            resp = sess.get(
                _PUBLIC_API,
                params={
                    "public_key": public_key,
                    "path": current,
                    "limit": limit,
                    "offset": offset,
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            embedded = data.get("_embedded", {}) or {}
            items = embedded.get("items", []) or []
            for item in items:
                item_type = item.get("type")
                if item_type == "dir":
                    if recursive:
                        to_visit.append(item.get("path", "/"))
                    continue
                if item_type != "file":
                    continue
                name = item.get("name", "")
                if Path(name).suffix.lower() not in _SUPPORTED_EXTS:
                    continue
                try:
                    modified = datetime.fromisoformat(
                        item.get("modified", "").replace("Z", "+00:00")
                    )
                except ValueError:
                    modified = datetime.now(timezone.utc)
                result.append(
                    YandexFile(
                        name=name,
                        path=item.get("path", "/"),
                        size=item.get("size", 0),
                        modified=modified,
                        parsed_date=parse_date_from_filename(name),
                    )
                )

            # Решаем, нужна ли следующая страница. Yandex возвращает
            # total/offset/limit в _embedded — если их нет (старое API
            # / неполный ответ), ориентируемся по фактическому числу
            # элементов.
            total = embedded.get("total")
            page_size = embedded.get("limit", limit)
            offset += page_size
            if total is not None:
                if offset >= total:
                    break
            else:
                if len(items) < limit:
                    break

    return result


def download_file(
    public_url: str,
    file_path: str,
    destination: Path,
    *,
    session: Optional[Union[requests.Session, RetryableSession]] = None,
) -> Path:
    """Скачать файл из публичной папки по внутреннему пути с retry."""
    sess = session or RetryableSession()
    close_session = session is None

    try:
        public_key, _ = split_public_url(public_url)

        # Получаем ссылку на скачивание с retry
        with sess:
            resp = sess.get(
                _DOWNLOAD_API,
                params={"public_key": public_key, "path": file_path},
                timeout=15,
            )
        resp.raise_for_status()
        href = resp.json().get("href")
        if not href:
            raise RuntimeError(
                f"Ответ Яндекс.Диска не содержит ссылки на скачивание: {resp.json()}"
            )

        # Скачиваем файл с retry
        with sess:
            dl = sess.get(href, stream=True, timeout=60)
        dl.raise_for_status()
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("wb") as f:
            for chunk in dl.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return destination
    finally:
        if close_session and hasattr(sess, '__exit__'):
            sess.__exit__(None, None, None)


def sync_folder(
    public_url: str,
    download_dir: Path,
    *,
    session: Optional[Union[requests.Session, RetryableSession]] = None,
    recursive: bool = False,
) -> List[tuple[YandexFile, Path]]:
    """
    Скачать все файлы с распознанной датой из публичной папки.

    Возвращает список ``(YandexFile, local_path)`` — уже скачанных и
    пригодных для импорта. Уже существующие файлы не перекачиваются
    (проверка по имени и размеру).
    """
    sess = session or RetryableSession()
    files = list_public_folder(public_url, session=sess, recursive=recursive)

    # Защита от тихой перезаписи: если в разных подпапках (recursive=True)
    # лежат файлы с одним именем — flatten в download_dir/<name> заставит
    # последний скачанный затереть предыдущий, и в манифест попадёт только
    # один. Если такое находим — берём более свежий по `modified` и
    # явно ругаемся в логе.
    by_name: Dict[str, YandexFile] = {}
    for f in files:
        if f.parsed_date is None:
            logger.info(
                "Пропускаем %s: не удалось распознать дату в имени файла", f.name
            )
            continue
        existing = by_name.get(f.name)
        if existing is None:
            by_name[f.name] = f
            continue
        if existing.path == f.path:
            # Один и тот же файл вернулся дважды (повторный обход) — не страшно.
            continue
        # Реальная коллизия — два файла с одинаковыми именами из разных папок.
        winner, loser = (
            (f, existing) if f.modified >= existing.modified else (existing, f)
        )
        logger.warning(
            "Коллизия имён на Яндекс.Диске: %s — %s (modified %s) и %s "
            "(modified %s). Импортируем более свежий, второй проигнорирован.",
            f.name,
            winner.path,
            winner.modified,
            loser.path,
            loser.modified,
        )
        by_name[f.name] = winner

    results: List[tuple[YandexFile, Path]] = []
    for f in by_name.values():
        local = download_dir / f.name
        if local.exists() and local.stat().st_size == f.size and f.size > 0:
            logger.info("Файл %s уже скачан, пропускаем", f.name)
        else:
            logger.info("Скачиваем %s (%d bytes)", f.name, f.size)
            download_file(public_url, f.path, local, session=sess)
        results.append((f, local))
    return results


_MANIFEST_NAME = ".imported.json"


def _manifest_path(download_dir: Path) -> Path:
    return download_dir / _MANIFEST_NAME


def _load_manifest(download_dir: Path) -> Dict[str, dict]:
    """Прочитать манифест уже импортированных файлов.

    Формат: ``{ "<filename>": {"size": int, "mtime": float,
    "schedule_date": "YYYY-MM-DD", "imported_at": "ISO timestamp"} }``.
    Если файла нет / он битый — возвращаем пустой словарь.
    """
    path = _manifest_path(download_dir)
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Манифест %s повреждён, игнорируем: %s", path, exc)
        return {}


def _save_manifest(download_dir: Path, manifest: Dict[str, dict]) -> None:
    path = _manifest_path(download_dir)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
    except OSError as exc:
        logger.warning("Не смогли сохранить манифест %s: %s", path, exc)


def _file_signature(path: Path) -> Tuple[int, int]:
    """Подпись файла: (size, mtime в наносекундах) — стабильна между
    запусками. Используется чтобы понять, изменился ли файл с прошлой
    успешной попытки импорта."""
    st = path.stat()
    return st.st_size, st.st_mtime_ns


def sync_and_import(
    public_url: str,
    download_dir: Path,
    *,
    recursive: bool = False,
) -> List[tuple[date, Path, int]]:
    """
    Скачать и импортировать все расписания из публичной папки.

    На каждом запуске пропускает файлы, которые уже были успешно
    импортированы и не менялись с тех пор (по размеру и mtime). Это
    избавляет от перепарсинга 200+ PDF при каждом рестарте бэкенда.

    Возвращает ``[(date, local_path, records_added), ...]``.
    Ошибки импорта не прерывают пайплайн — они логируются, и процесс
    продолжает работу с остальными файлами.
    """
    from app.utils.import_schedule import import_schedule

    manifest = _load_manifest(download_dir)
    summary: List[tuple[date, Path, int]] = []
    skipped_unchanged = 0
    for f, local in sync_folder(public_url, download_dir, recursive=recursive):
        try:
            size, mtime_ns = _file_signature(local)
        except OSError:
            # Файла внезапно нет — пробуем импортировать по существующему пути,
            # пусть импортер сам ругнётся.
            size, mtime_ns = 0, 0

        entry = manifest.get(f.name)
        if (
            entry is not None
            and entry.get("size") == size
            and entry.get("mtime_ns") == mtime_ns
            and entry.get("schedule_date") == f.parsed_date.isoformat()
        ):
            skipped_unchanged += 1
            continue

        try:
            added = import_schedule(
                str(local), f.parsed_date.strftime("%Y-%m-%d")
            )
            summary.append((f.parsed_date, local, added or 0))
            manifest[f.name] = {
                "size": size,
                "mtime_ns": mtime_ns,
                "schedule_date": f.parsed_date.isoformat(),
                "imported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
        except Exception as exc:
            logger.error(
                "Ошибка импорта %s (%s): %s", f.name, f.parsed_date, exc
            )

    if skipped_unchanged:
        logger.info(
            "⏭ Пропущено %d файлов без изменений (уже импортированы ранее)",
            skipped_unchanged,
        )

    _save_manifest(download_dir, manifest)
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
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Обходить вложенные подпапки (архивы по месяцам и т.п.).",
    )
    args = parser.parse_args()

    if not args.url:
        parser.error(
            "Требуется публичная ссылка на папку (--url или переменная окружения "
            "YANDEX_DISK_PUBLIC_URL)."
        )

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if args.list_only:
        for f in list_public_folder(args.url, recursive=args.recursive):
            print(f"{str(f.parsed_date) if f.parsed_date else '??':10}  "
                  f"{f.size:>10}  {f.name}")
        return

    dest = Path(args.dest)
    summary = sync_and_import(args.url, dest, recursive=args.recursive)
    print(f"Готово. Обработано файлов: {len(summary)}")
    for day, path, added in summary:
        print(f"  {day.isoformat()}  {path.name}  +{added} записей")


if __name__ == "__main__":
    _main()
