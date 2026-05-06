"""
Утилиты для retry механизма с использованием tenacity.
"""
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    RetryError
)
import requests
import logging
from functools import wraps
from app.core.config import settings

logger = logging.getLogger(__name__)

# Стандартные HTTP ошибки, которые можно retry-ить
RETRYABLE_HTTP_ERRORS = (
    requests.exceptions.Timeout,
    requests.exceptions.ConnectionError,
    requests.exceptions.HTTPError,
)

# HTTP статусы, при которых стоит retry-ить
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def retryable_request(max_retries=None, retry_delay=None):
    """
    Декоратор для retry HTTP запросов.

    Args:
        max_retries: Максимальное количество попыток (default из settings)
        retry_delay: Начальная задержка между попытками (default из settings)
    """
    max_retries = max_retries or settings.EXTERNAL_API_MAX_RETRIES
    retry_delay = retry_delay or settings.EXTERNAL_API_RETRY_DELAY

    def decorator(func):
        @retry(
            stop=stop_after_attempt(max_retries),
            wait=wait_exponential(multiplier=retry_delay, min=retry_delay, max=60),
            retry=retry_if_exception_type(RETRYABLE_HTTP_ERRORS),
            before_sleep=before_sleep_log(logger, logging.WARNING),
            reraise=True
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


class RetryableSession:
    """HTTP Session с автоматическим retry."""

    def __init__(self, max_retries=None, timeout=None):
        self.max_retries = max_retries or settings.EXTERNAL_API_MAX_RETRIES
        self.timeout = timeout or settings.EXTERNAL_API_TIMEOUT
        self.session = requests.Session()

    def _should_retry(self, response):
        """Проверяет, стоит ли retry-ить ответ."""
        if response.status_code in RETRYABLE_STATUS_CODES:
            return True
        try:
            response.raise_for_status()
            return False
        except requests.HTTPError:
            return response.status_code >= 500

    def request(self, method, url, **kwargs):
        """Выполняет HTTP запрос с retry."""
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                # Устанавливаем timeout если не задан
                if 'timeout' not in kwargs:
                    kwargs['timeout'] = self.timeout

                response = self.session.request(method, url, **kwargs)

                if not self._should_retry(response):
                    return response

                logger.warning(
                    f"Retryable status {response.status_code} from {url}, "
                    f"attempt {attempt + 1}/{self.max_retries}"
                )

                if attempt < self.max_retries - 1:
                    import time
                    wait_time = min(2 ** attempt, 60)  # exponential backoff
                    time.sleep(wait_time)

            except RETRYABLE_HTTP_ERRORS as e:
                last_exception = e
                logger.warning(
                    f"Request failed to {url}: {e}, attempt {attempt + 1}/{self.max_retries}"
                )
                if attempt < self.max_retries - 1:
                    import time
                    wait_time = min(2 ** attempt, 60)
                    time.sleep(wait_time)

        if last_exception:
            raise last_exception
        return response

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.session.close()
