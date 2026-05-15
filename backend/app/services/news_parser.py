"""
Сервис для парсинга новостей с сайта ККРИТ
"""
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional
import logging
from app.utils.retry import RetryableSession

logger = logging.getLogger(__name__)

# URL страницы новостей колледжа
NEWS_URL = "https://kraskrit.ru/news/"

# User-Agent для избежания блокировки
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def fetch_news_from_website() -> List[Dict]:
    """
    Загружает и парсит новости с сайта колледжа с автоматическим retry.

    Returns:
        List[Dict]: Список словарей с данными новостей
    """
    try:
        logger.info(f"Загрузка новостей с {NEWS_URL}")

        with RetryableSession() as session:
            response = session.get(NEWS_URL, headers=HEADERS)
            response.raise_for_status()
            html = response.text

        news_list = parse_news_html(html)

        logger.info(f"Успешно загружено {len(news_list)} новостей")
        return news_list

    except Exception as e:
        logger.error(f"Ошибка при загрузке новостей: {e}")
        return []


def parse_news_html(html: str) -> List[Dict]:
    """
    Парсит HTML и извлекает данные новостей

    Args:
        html: HTML-код страницы

    Returns:
        List[Dict]: Список новостей
    """
    soup = BeautifulSoup(html, 'lxml')
    news_list = []

    # TODO: Адаптировать селекторы под реальную структуру сайта
    # Это примерная структура, нужно исследовать реальный HTML

    # Пример: ищем все блоки новостей
    news_blocks = soup.find_all('div', class_='news-item')  # Нужно уточнить класс

    if not news_blocks:
        # Альтернативные селекторы
        news_blocks = soup.find_all('article')

    for block in news_blocks[:10]:  # Берем максимум 10 последних новостей
        try:
            news_data = extract_news_data(block)
            if news_data:
                news_list.append(news_data)
        except Exception as e:
            logger.warning(f"Ошибка при обработке блока новости: {e}")
            continue

    return news_list


def extract_news_data(block) -> Optional[Dict]:
    """
    Извлекает данные из блока новости

    Args:
        block: BeautifulSoup элемент с новостью

    Returns:
        Dict или None: Данные новости
    """
    try:
        # Извлекаем заголовок
        title_elem = block.find(['h2', 'h3', 'h4'])
        if not title_elem:
            return None
        title = title_elem.get_text(strip=True)

        # Извлекаем описание
        description_elem = block.find(['p', 'div'], class_=['description', 'excerpt', 'summary'])
        description = description_elem.get_text(strip=True) if description_elem else ""

        # Извлекаем ссылку
        link_elem = block.find('a', href=True)
        source_url = link_elem['href'] if link_elem else ""
        if source_url and not source_url.startswith('http'):
            source_url = f"https://kraskrit.ru{source_url}"

        # Извлекаем дату
        date_elem = block.find(['time', 'span'], class_=['date', 'published'])
        published_date = parse_date(date_elem.get_text(strip=True)) if date_elem else datetime.now()

        # Определяем иконку по ключевым словам
        icon = determine_icon(title + " " + description)

        return {
            'title': title,
            'description': description[:500],  # Ограничиваем длину
            'icon': icon,
            'published_date': published_date,
            'source_url': source_url,
            'is_active': True
        }

    except Exception as e:
        logger.error(f"Ошибка извлечения данных: {e}")
        return None


def parse_date(date_str: str) -> datetime:
    """
    Парсит строку с датой в datetime

    Args:
        date_str: Строка с датой

    Returns:
        datetime: Объект даты
    """
    # Попытка распарсить различные форматы дат
    formats = [
        '%d.%m.%Y',
        '%d/%m/%Y',
        '%Y-%m-%d',
        '%d %B %Y',
        '%d %b %Y'
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # Если не удалось распарсить, возвращаем текущую дату
    return datetime.now()


def determine_icon(text: str) -> str:
    """
    Определяет подходящую иконку на основе текста новости

    Args:
        text: Текст новости

    Returns:
        str: Эмодзи-иконка
    """
    text_lower = text.lower()

    if any(word in text_lower for word in ['олимпиада', 'конкурс', 'победа', 'призер', 'награ']):
        return '🏆'
    elif any(word in text_lower for word in ['день открытых дверей', 'абитуриент', 'поступ']):
        return '🎓'
    elif any(word in text_lower for word in ['мероприятие', 'событие', 'праздник']):
        return '🎉'
    elif any(word in text_lower for word in ['учеб', 'занятие', 'курс', 'специальность']):
        return '📚'
    elif any(word in text_lower for word in ['спорт', 'соревнование']):
        return '⚽'
    else:
        return '📰'


def save_news_to_db(news_list: List[Dict], db_session):
    """
    Сохраняет новости в базу данных

    Args:
        news_list: Список новостей
        db_session: Сессия базы данных
    """
    from app.models.news import News

    saved_count = 0

    for news_data in news_list:
        try:
            # Проверяем, существует ли уже такая новость
            existing = db_session.query(News).filter(
                News.title == news_data['title']
            ).first()

            if existing:
                # Обновляем существующую
                for key, value in news_data.items():
                    setattr(existing, key, value)
                existing.updated_at = datetime.utcnow()
            else:
                # Создаем новую
                news = News(**news_data)
                db_session.add(news)

            saved_count += 1

        except Exception as e:
            logger.error(f"Ошибка сохранения новости '{news_data.get('title')}': {e}")
            continue

    try:
        db_session.commit()
        logger.info(f"Сохранено/обновлено {saved_count} новостей")
    except Exception as e:
        logger.error(f"Ошибка при коммите в БД: {e}")
        db_session.rollback()


if __name__ == "__main__":
    # Для тестирования парсера
    logging.basicConfig(level=logging.INFO)
    news = fetch_news_from_website()
    for item in news:
        print(f"\n{item['icon']} {item['title']}")
        print(f"   {item['description'][:100]}...")
        print(f"   {item['source_url']}")
