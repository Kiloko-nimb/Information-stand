"""
Утилита для парсинга PDF с расписанием
"""
import pdfplumber
from typing import List, Dict

class ScheduleParser:
    """Парсер расписания из PDF"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def parse(self) -> List[Dict]:
        """
        Парсит PDF и возвращает список занятий

        Returns:
            List[Dict]: Список словарей с данными о занятиях
        """
        schedule_data = []

        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                # Извлекаем таблицы со страницы
                tables = page.extract_tables()

                for table in tables:
                    # Обработка таблицы
                    # TODO: Реализовать логику парсинга в зависимости от формата PDF ККРИТ
                    pass

        return schedule_data

    def extract_group_schedule(self, group_name: str) -> List[Dict]:
        """Извлекает расписание для конкретной группы"""
        all_schedule = self.parse()
        return [item for item in all_schedule if item.get('group') == group_name]
