"""
Сервис для парсинга новостей колледжа.

Основной источник: RSS-лента сайта kraskrit.ru (https://kraskrit.ru/feed/).
RSS даёт чистые данные без скрапинга HTML, включая ссылки на оригинальные
посты и встроенные изображения (через тег <content:encoded>).

Группа ВК (https://vk.com/kraskrit) дублирует те же новости, поэтому
RSS — самый надёжный способ их получить без авторизации в VK API.
Когда у проекта появится сервисный токен VK, можно будет добавить
прямой парсинг стены через метод wall.get (см. функцию-заглушку
fetch_news_from_vk_api ниже).
"""
import re
import logging
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.models.news import News

logger = logging.getLogger(__name__)

RSS_URL = "https://kraskrit.ru/feed/"
SITE_BASE = "https://kraskrit.ru"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
}

# Namespaces RSS-фида WordPress
NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def _strip_html(html: str) -> str:
    """Убираем HTML-теги и схлопываем пробелы."""
    if not html:
        return ""
    text = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text).strip()


def _extract_first_image(html: str) -> Optional[str]:
    """Возвращает первую картинку из HTML-блока (если есть)."""
    if not html:
        return None
    match = re.search(r'<img[^>]+src="([^"]+)"', html)
    return match.group(1) if match else None


def _fetch_article_image(article_url: str) -> Optional[str]:
    """Если в RSS не было картинки — забираем og:image со страницы статьи."""
    try:
        resp = requests.get(article_url, headers=HEADERS, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        og = soup.find("meta", attrs={"property": "og:image"})
        if og and og.get("content"):
            return og["content"]
        # fallback: первая <img> в content article
        article = soup.find("article") or soup.find("main") or soup
        img = article.find("img")
        if img and img.get("src"):
            return img["src"]
    except Exception as exc:
        logger.debug("Не удалось получить картинку для %s: %s", article_url, exc)
    return None


def fetch_news_from_website() -> List[Dict]:
    """
    Загружает RSS-фид сайта колледжа и формирует список новостей,
    готовый для сохранения в БД.
    """
    logger.info("Загрузка новостей из RSS: %s", RSS_URL)
    try:
        resp = requests.get(RSS_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as exc:
        logger.error("Не удалось получить RSS: %s", exc)
        return []

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as exc:
        logger.error("RSS невалидный: %s", exc)
        return []

    items = root.findall(".//item")
    news_list: List[Dict] = []

    for item in items[:8]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue

        # content:encoded — полный HTML поста, description — краткий
        content_html = item.findtext("content:encoded", default="", namespaces=NS) or ""
        desc_html = item.findtext("description", default="") or ""

        text = _strip_html(content_html) or _strip_html(desc_html)
        if len(text) > 280:
            text = text[:277].rstrip() + "…"

        image_url = (
            _extract_first_image(content_html)
            or _extract_first_image(desc_html)
            or _fetch_article_image(link)
        )

        pub_raw = item.findtext("pubDate") or ""
        try:
            published = parsedate_to_datetime(pub_raw).replace(tzinfo=None) if pub_raw else datetime.utcnow()
        except Exception:
            published = datetime.utcnow()

        news_list.append(
            {
                "title": title[:255],
                "description": text or title,
                "icon": "📰",
                "published_date": published,
                "source_url": link,
                "image_url": image_url,
            }
        )

    logger.info("Получено новостей: %d", len(news_list))
    return news_list


def save_news_to_db(news_list: List[Dict], db: Session) -> None:
    """
    Сохраняет/обновляет новости в БД, используя source_url как
    уникальный идентификатор.
    """
    if not news_list:
        return

    try:
        for item in news_list:
            existing = (
                db.query(News).filter(News.source_url == item["source_url"]).first()
            )
            if existing:
                existing.title = item["title"]
                existing.description = item["description"]
                existing.image_url = item["image_url"]
                existing.published_date = item["published_date"]
                existing.is_active = True
            else:
                db.add(
                    News(
                        title=item["title"],
                        description=item["description"],
                        icon=item["icon"],
                        published_date=item["published_date"],
                        source_url=item["source_url"],
                        image_url=item["image_url"],
                        is_active=True,
                    )
                )
        db.commit()
    except Exception as exc:
        logger.error("Ошибка при сохранении новостей: %s", exc)
        db.rollback()


def fetch_news_from_vk_api(access_token: str, domain: str = "kraskrit", count: int = 10) -> List[Dict]:
    """
    Опциональный источник: VK API (wall.get).

    Требует сервисный/пользовательский токен VK. Когда токен будет
    добавлен (например, через переменную окружения VK_SERVICE_TOKEN),
    эту функцию можно подключить к фоновому таску в main.py.
    """
    if not access_token:
        return []
    try:
        resp = requests.get(
            "https://api.vk.com/method/wall.get",
            params={
                "domain": domain,
                "count": count,
                "v": "5.131",
                "access_token": access_token,
            },
            timeout=15,
        )
        data = resp.json()
        posts = data.get("response", {}).get("items", [])
    except Exception as exc:
        logger.error("VK API недоступен: %s", exc)
        return []

    news_list: List[Dict] = []
    for post in posts:
        text = (post.get("text") or "").strip()
        if not text:
            continue

        title = " ".join(text.split()[:8])
        if len(title) < 5:
            continue

        image_url = None
        for attach in post.get("attachments", []):
            if attach.get("type") == "photo":
                sizes = attach.get("photo", {}).get("sizes", [])
                if sizes:
                    image_url = sorted(sizes, key=lambda s: s.get("width", 0))[-1].get("url")
                    break

        published = datetime.utcfromtimestamp(post.get("date", 0)) if post.get("date") else datetime.utcnow()
        source_url = f"https://vk.com/wall{post.get('owner_id')}_{post.get('id')}"

        news_list.append(
            {
                "title": title[:255],
                "description": text[:280],
                "icon": "📰",
                "published_date": published,
                "source_url": source_url,
                "image_url": image_url,
            }
        )

    return news_list


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    items = fetch_news_from_website()
    for n in items:
        print(f"\n{n['icon']} {n['title']}")
        print(f"   IMG: {n['image_url']}")
        print(f"   {n['description'][:120]}")
        print(f"   {n['source_url']} | {n['published_date']}")
