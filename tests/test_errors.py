import pytest

from src.url_normalizer.errors import InvalidURLError
from src.url_normalizer.normalizer import normalize


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.com",
        "javascript:alert(1)",
        "file:///etc/passwd",
        "just text",
        "http://",
    ],
)
def test_normalize_rejects_invalid_urls(url):
    with pytest.raises(InvalidURLError):
        normalize(url)
