"""Тесты для модуля синхронизации с Яндекс.Диском.

Не делаем сетевых запросов: все вызовы `requests` подменяются через monkeypatch.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from app.services import yandex_disk


def test_parse_date_dot_format():
    assert yandex_disk.parse_date_from_filename("13.04.2026.pdf") == date(2026, 4, 13)


def test_parse_date_dash_format():
    assert yandex_disk.parse_date_from_filename(
        "raspisanie-13-04-2026.xlsx"
    ) == date(2026, 4, 13)


def test_parse_date_underscore_format():
    assert yandex_disk.parse_date_from_filename(
        "schedule_13_04_2026_final.pdf"
    ) == date(2026, 4, 13)


def test_parse_date_unknown_format():
    assert yandex_disk.parse_date_from_filename("schedule-april-2026.pdf") is None


def test_parse_date_invalid_date():
    """32-е февраля не существует — возвращаем None."""
    assert yandex_disk.parse_date_from_filename("32.02.2026.pdf") is None


def test_split_public_url_root():
    root, inner = yandex_disk.split_public_url("https://disk.yandex.ru/d/abc123")
    assert root == "https://disk.yandex.ru/d/abc123"
    assert inner == "/"


def test_split_public_url_subfolder():
    root, inner = yandex_disk.split_public_url(
        "https://disk.yandex.ru/d/abc123/корпус%20156"
    )
    assert root == "https://disk.yandex.ru/d/abc123"
    # URL-decoded:
    assert inner == "/корпус 156"


def test_split_public_url_deep_subfolder():
    root, inner = yandex_disk.split_public_url(
        "https://disk.yandex.ru/d/abc123/sub/nested/file.pdf"
    )
    assert root == "https://disk.yandex.ru/d/abc123"
    assert inner == "/sub/nested/file.pdf"


class _FakeResponse:
    def __init__(self, payload: dict | None = None, content: bytes = b""):
        self._payload = payload or {}
        self._content = content
        self.status_code = 200

    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return self._payload

    def iter_content(self, chunk_size: int = 8192):
        yield self._content


class _FakeSession:
    def __init__(self, list_payload: dict, download_payload: dict, file_bytes: bytes):
        self.list_payload = list_payload
        self.download_payload = download_payload
        self.file_bytes = file_bytes
        self.calls: list[tuple[str, dict]] = []

    def get(self, url, params=None, timeout=None, stream=False):
        self.calls.append((url, params or {}))
        if url.endswith("/public/resources"):
            return _FakeResponse(self.list_payload)
        if url.endswith("/public/resources/download"):
            return _FakeResponse(self.download_payload)
        # Финальный редирект на скачивание.
        return _FakeResponse(content=self.file_bytes)


def test_list_public_folder_filters_supported_extensions():
    session = _FakeSession(
        list_payload={
            "_embedded": {
                "items": [
                    {
                        "type": "file",
                        "name": "13.04.2026.xlsx",
                        "path": "/13.04.2026.xlsx",
                        "size": 1234,
                        "modified": "2026-04-01T09:00:00+00:00",
                    },
                    {
                        "type": "file",
                        "name": "readme.txt",  # игнорируется
                        "path": "/readme.txt",
                        "size": 10,
                        "modified": "2026-04-01T09:00:00+00:00",
                    },
                    {
                        "type": "dir",  # директории игнорируются
                        "name": "subfolder",
                        "path": "/subfolder",
                        "size": 0,
                        "modified": "2026-04-01T09:00:00+00:00",
                    },
                    {
                        "type": "file",
                        "name": "schedule.pdf",  # без даты → path есть, дата None
                        "path": "/schedule.pdf",
                        "size": 500,
                        "modified": "2026-04-01T09:00:00+00:00",
                    },
                ]
            }
        },
        download_payload={},
        file_bytes=b"",
    )

    files = yandex_disk.list_public_folder("https://disk.yandex.ru/d/abc", session=session)
    names = [f.name for f in files]
    assert names == ["13.04.2026.xlsx", "schedule.pdf"]
    assert files[0].parsed_date == date(2026, 4, 13)
    assert files[1].parsed_date is None


def test_sync_folder_downloads_files(tmp_path: Path):
    session = _FakeSession(
        list_payload={
            "_embedded": {
                "items": [
                    {
                        "type": "file",
                        "name": "13.04.2026.pdf",
                        "path": "/13.04.2026.pdf",
                        "size": 5,
                        "modified": "2026-04-01T09:00:00+00:00",
                    },
                    {
                        "type": "file",
                        "name": "no-date.xlsx",  # пропускается — нет даты
                        "path": "/no-date.xlsx",
                        "size": 5,
                        "modified": "2026-04-01T09:00:00+00:00",
                    },
                ]
            }
        },
        download_payload={"href": "https://example.com/signed-url"},
        file_bytes=b"hello",
    )

    results = yandex_disk.sync_folder(
        "https://disk.yandex.ru/d/abc", tmp_path, session=session
    )

    assert len(results) == 1
    downloaded = results[0][1]
    assert downloaded.exists()
    assert downloaded.read_bytes() == b"hello"
    assert downloaded.name == "13.04.2026.pdf"


def test_sync_folder_skips_existing_file(tmp_path: Path):
    """Если файл уже скачан и размер совпадает — не скачиваем повторно."""
    existing = tmp_path / "13.04.2026.pdf"
    existing.write_bytes(b"already-here")

    session = _FakeSession(
        list_payload={
            "_embedded": {
                "items": [
                    {
                        "type": "file",
                        "name": "13.04.2026.pdf",
                        "path": "/13.04.2026.pdf",
                        "size": len(b"already-here"),
                        "modified": "2026-04-01T09:00:00+00:00",
                    }
                ]
            }
        },
        download_payload={"href": "https://example.com/signed-url"},
        file_bytes=b"",
    )

    results = yandex_disk.sync_folder(
        "https://disk.yandex.ru/d/abc", tmp_path, session=session
    )

    assert len(results) == 1
    # Проверяем, что за скачиванием в Яндекс-API не ходили.
    called_paths = [c[0] for c in session.calls]
    assert not any("download" in p for p in called_paths)


def test_sync_and_import_skips_unchanged_files(tmp_path: Path, monkeypatch):
    """На втором запуске неизменённый файл не должен повторно
    проходить через ``import_schedule`` — иначе на каждом рестарте
    бэкенда мы перепарсим 200 PDF без причины."""
    pdf = tmp_path / "13.04.2026.pdf"
    pdf.write_bytes(b"fake-pdf-bytes")

    list_payload = {
        "_embedded": {
            "items": [
                {
                    "type": "file",
                    "name": "13.04.2026.pdf",
                    "path": "/13.04.2026.pdf",
                    "size": len(b"fake-pdf-bytes"),
                    "modified": "2026-04-01T09:00:00+00:00",
                }
            ]
        }
    }

    def make_session():
        return _FakeSession(
            list_payload=list_payload,
            download_payload={"href": "https://example.com/dl"},
            file_bytes=b"",
        )

    import_calls: list[tuple[str, str]] = []

    def fake_import(file_path, date_str):
        import_calls.append((file_path, date_str))
        return 42

    # Подменяем импорт расписания на «заглушку».
    import app.utils.import_schedule as import_module

    monkeypatch.setattr(import_module, "import_schedule", fake_import)

    # Первый запуск — должно вызваться import_schedule.
    monkeypatch.setattr(yandex_disk.requests, "Session", make_session)
    summary = yandex_disk.sync_and_import(
        "https://disk.yandex.ru/d/abc", tmp_path
    )
    assert len(summary) == 1
    assert summary[0][2] == 42
    assert len(import_calls) == 1
    assert (tmp_path / ".imported.json").exists()

    # Второй запуск без изменений — import_schedule вызываться НЕ должен.
    summary2 = yandex_disk.sync_and_import(
        "https://disk.yandex.ru/d/abc", tmp_path
    )
    assert summary2 == []
    assert len(import_calls) == 1, "import_schedule повторно не должен вызываться"

    # А если файл "изменился" (mtime + размер) — должен импортироваться снова.
    pdf.write_bytes(b"fake-pdf-bytes-v2")
    list_payload["_embedded"]["items"][0]["size"] = len(b"fake-pdf-bytes-v2")
    summary3 = yandex_disk.sync_and_import(
        "https://disk.yandex.ru/d/abc", tmp_path
    )
    assert len(summary3) == 1
    assert len(import_calls) == 2
