import pytest

from url_normalizer.normalizer import normalize


@pytest.mark.parametrize(
    "url",
    [
        "https://youtube.com/watch?v=abc123",
        "https://www.youtube.com/watch?v=abc123&feature=share",
        "https://www.youtube.com/shorts/abc123",
        "https://old.reddit.com/r/python/comments/xyz/title/",
        "https://m.reddit.com/r/python/comments/xyz/title",
        "https://reddit.com/r/python/comments/xyz/title",
    ],
)
def test_idempotency(url):
    assert normalize(normalize(url)) == normalize(url)
