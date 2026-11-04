import pytest

from url_normalizer.normalizer import extract_id, normalize


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        # Короткая ссылка youtu.be
        (
            "https://youtu.be/abc123",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Обычная ссылка на видео
        (
            "https://youtube.com/watch?v=abc123",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Ссылка с дополнительным параметром
        (
            "https://www.youtube.com/watch?v=abc123&feature=share",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Мобильная версия
        (
            "https://m.youtube.com/watch?v=abc123",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # YouTube Music
        (
            "https://music.youtube.com/watch?v=abc123",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Shorts
        (
            "https://www.youtube.com/shorts/abc123",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Embed
        (
            "https://www.youtube.com/embed/abc123",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Live
        (
            "https://www.youtube.com/live/abc123",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Удаление таймкода t
        (
            "https://www.youtube.com/watch?v=abc123&t=120",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Удаление таймкода start
        (
            "https://www.youtube.com/watch?v=abc123&start=120",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Удаление параметров плейлиста у ссылки на видео
        (
            "https://www.youtube.com/watch?v=abc123&list=playlist123&index=2",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Удаление трекинг-параметров
        (
            "https://youtu.be/abc123?utm_source=telegram",
            "https://www.youtube.com/watch?v=abc123",
        ),
        # Плейлист сохраняет параметр list
        (
            "https://www.youtube.com/playlist?list=playlist123",
            "https://www.youtube.com/playlist?list=playlist123",
        ),
        # url без id
        (
            "https://youtube.com/",
            "https://www.youtube.com/",
        ),
    ],
)
def test_normalize_youtube_urls(url, expected):
    assert normalize(url) == expected


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        (
            "https://youtu.be/abc123",
            "abc123",
        ),
        (
            "https://www.youtube.com/watch?v=abc123",
            "abc123",
        ),
        (
            "https://m.youtube.com/watch?v=abc123",
            "abc123",
        ),
        (
            "https://www.youtube.com/shorts/abc123",
            "abc123",
        ),
        (
            "https://www.youtube.com/embed/abc123",
            "abc123",
        ),
        (
            "https://www.youtube.com/live/abc123",
            "abc123",
        ),
        # Для плейлиста ID видео отсутствует
        (
            "https://www.youtube.com/playlist?list=playlist123",
            None,
        ),
        # Для обычной страницы канала ID видео отсутствует
        (
            "https://www.youtube.com/@somechannel",
            None,
        ),
    ],
)
def test_extract_youtube_id(url, expected):
    assert extract_id(url) == expected
