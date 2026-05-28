import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.news import News

logger = logging.getLogger(__name__)

def fetch_news_from_website():
    """
    Парсит новости из публичной группы ВКонтакте: https://vk.com/kraskrit
    Использует мобильную версию (m.vk.com) для упрощения извлечения данных без API.
    """
    url = "https://m.vk.com/kraskrit"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # В мобильной версии посты лежат в элементах с классом wall_item
        posts = soup.find_all('div', class_='wall_item')
        
        news_list = []
        
        for post in posts[:10]:  # Берем последние 10 постов
            # Ищем текст поста
            text_element = post.find('div', class_='pi_text')
            if not text_element:
                continue
                
            description = text_element.get_text(strip=True, separator=' ')
            
            # Если текст слишком короткий, пропускаем (например, только репост без текста)
            if len(description) < 10:
                continue

            # Генерируем заголовок из первых слов
            words = description.split()
            title = ' '.join(words[:7]) + '...' if len(words) > 7 else description
            
            # Ищем картинки (в мобильной версии это теги img внутри thumb_map)
            image_url = None
            img_element = post.find('img', class_='thumb_map_img') or post.find('img', class_='thumb_item')
            if img_element and img_element.get('src'):
                image_url = img_element.get('src')
            
            # Извлекаем ссылку на сам пост
            post_link = post.find('a', class_='pi_link')
            source_url = None
            if post_link and post_link.get('href'):
                source_url = "https://vk.com" + post_link.get('href')
                
            # Дата публикации (приблизительная для парсера)
            date_element = post.find('a', class_='wi_date')
            published_date = datetime.utcnow()
            
            news_list.append({
                "title": title,
                "description": description,
                "icon": "📰",
                "published_date": published_date,
                "source_url": source_url or "https://vk.com/kraskrit",
                "image_url": image_url
            })
            
        return news_list

    except Exception as e:
        logger.error(f"Ошибка при парсинге новостей ВК: {e}")
        return []

def save_news_to_db(news_list: list, db: Session):
    """
    Сохраняет новости в базу данных.
    Если новость с таким же заголовком/описанием существует, обновляет ее.
    """
    for item in news_list:
        # Проверяем, есть ли уже такая новость (по заголовку или источнику)
        existing_news = db.query(News).filter(
            (News.title == item['title']) | 
            ((News.source_url == item['source_url']) & (News.source_url != "https://vk.com/kraskrit"))
        ).first()

        if existing_news:
            # Обновляем
            existing_news.description = item['description']
            existing_news.image_url = item['image_url']
            existing_news.published_date = item['published_date']
        else:
            # Создаем новую
            new_news = News(
                title=item['title'],
                description=item['description'],
                icon=item['icon'],
                published_date=item['published_date'],
                source_url=item['source_url'],
                image_url=item['image_url']
            )
            db.add(new_news)

    db.commit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    news = fetch_news_from_website()
    for item in news:
        print(f"\n{item['icon']} {item['title']}")
        print(f"   Image: {item['image_url']}")
        print(f"   {item['description'][:100]}...")
        print(f"   {item['source_url']}")
