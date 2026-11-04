import pytest

from url_normalizer.sources import Source, detect_source


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        # YouTube
        ("https://youtube.com", Source.YOUTUBE),
        ("https://www.youtube.com", Source.YOUTUBE),
        ("https://m.youtube.com", Source.YOUTUBE),
        ("https://music.youtube.com", Source.YOUTUBE),
        ("https://youtu.be/abc123", Source.YOUTUBE),
        ("http://youtube.com", Source.YOUTUBE),
        ("http://www.youtube.com", Source.YOUTUBE),
        ("http://m.youtube.com", Source.YOUTUBE),
        ("http://music.youtube.com", Source.YOUTUBE),
        ("http://youtu.be/abc123", Source.YOUTUBE),
        # Reddit
        ("https://reddit.com", Source.REDDIT),
        ("https://www.reddit.com", Source.REDDIT),
        ("https://old.reddit.com", Source.REDDIT),
        ("https://m.reddit.com", Source.REDDIT),
        ("https://redd.it/abc123", Source.REDDIT),
        ("http://reddit.com", Source.REDDIT),
        ("http://www.reddit.com", Source.REDDIT),
        ("http://old.reddit.com", Source.REDDIT),
        ("http://m.reddit.com", Source.REDDIT),
        ("http://redd.it/abc123", Source.REDDIT),
        # Generic
        ("https://google.com", Source.GENERIC),
        ("https://example.com", Source.GENERIC),
        ("https://github.com", Source.GENERIC),
        ("http://google.com", Source.GENERIC),
        ("http://example.com", Source.GENERIC),
        ("http://github.com", Source.GENERIC),
        # Поддельные домены — должны быть Generic
        ("https://youtube.com.evil.example", Source.GENERIC),
        ("https://notyoutube.com", Source.GENERIC),
        ("https://reddit.com.evil.example", Source.GENERIC),
        ("https://fake-reddit.com", Source.GENERIC),
        ("http://youtube.com.evil.example", Source.GENERIC),
        ("http://notyoutube.com", Source.GENERIC),
        ("http://reddit.com.evil.example", Source.GENERIC),
        ("http://fake-reddit.com", Source.GENERIC),
    ],
)
def test_detect_source(url, expected):
    assert detect_source(url) == expected
