import pytest

from src.url_normalizer.normalizer import extract_id
from url_normalizer.normalizer import normalize


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        # Старый домен Reddit
        (
            "https://old.reddit.com/r/python/comments/xyz/title/",
            "https://www.reddit.com/r/python/comments/xyz/",
        ),
        # Обычный домен Reddit
        (
            "https://reddit.com/r/python/comments/xyz/title",
            "https://www.reddit.com/r/python/comments/xyz/",
        ),
        # Сохранение регистра названия сабреддита
        (
            "https://reddit.com/r/Python/comments/xyz/some_title",
            "https://www.reddit.com/r/Python/comments/xyz/",
        ),
        # Мобильный домен
        (
            "https://m.reddit.com/r/python/comments/xyz/title",
            "https://www.reddit.com/r/python/comments/xyz/",
        ),
        # www-домен
        (
            "https://www.reddit.com/r/python/comments/xyz/title",
            "https://www.reddit.com/r/python/comments/xyz/",
        ),
        # Удаление трекинг-параметров
        (
            "https://old.reddit.com/r/python/comments/xyz/title/?utm_medium=android",
            "https://www.reddit.com/r/python/comments/xyz/",
        ),
        # Короткая ссылка не раскрывается
        (
            "https://redd.it/xyz",
            "https://redd.it/xyz",
        ),
    ],
)
def test_normalize_reddit_urls(url, expected):
    assert normalize(url) == expected


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "https://reddit.com/r/python/comments/xyz/title",
            "xyz",
        ),
        (
            "https://www.reddit.com/r/Python/comments/xyz/",
            "xyz",
        ),
        (
            "https://old.reddit.com/r/python/comments/xyz/title/",
            "xyz",
        ),
        (
            "https://m.reddit.com/r/python/comments/xyz/title",
            "xyz",
        ),
        # Короткая ссылка
        (
            "https://redd.it/xyz",
            "xyz",
        ),
    ],
)
def test_extract_reddit_id(url, expected):
    assert extract_id(url) == expected
