import pytest

from url_normalizer.normalizer import normalize


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        # 1. Удаление пробелов по краям
        (
            "  https://example.com/page  ",
            "https://example.com/page",
        ),
        # 2. Приведение схемы и домена к нижнему регистру
        (
            "HTTPS://EXAMPLE.COM",
            "https://example.com/",
        ),
        (
            "http://Example.COM",
            "http://example.com/",
        ),
        # 3. Удаление портов по умолчанию
        (
            "https://example.com:443/page",
            "https://example.com/page",
        ),
        (
            "http://example.com:80/page",
            "http://example.com/page",
        ),
        # 4. Удаление фрагмента
        (
            "https://example.com/page#section",
            "https://example.com/page",
        ),
        (
            "https://example.com/page?key=value#section",
            "https://example.com/page?key=value",
        ),
        # 5. Удаление tracking-параметров
        (
            "https://example.com/page?utm_source=telegram",
            "https://example.com/page",
        ),
        (
            "https://example.com/page?utm_medium=social",
            "https://example.com/page",
        ),
        (
            "https://example.com/page?fbclid=123",
            "https://example.com/page",
        ),
        (
            "https://example.com/page?gclid=123",
            "https://example.com/page",
        ),
        (
            "https://example.com/page?yclid=123",
            "https://example.com/page",
        ),
        (
            "https://example.com/page?mc_cid=123",
            "https://example.com/page",
        ),
        (
            "https://example.com/page?mc_eid=123",
            "https://example.com/page",
        ),
        # 6. Сортировка остальных параметров по имени
        (
            "https://example.com/page?b=2&a=1",
            "https://example.com/page?a=1&b=2",
        ),
        (
            "https://example.com/page?z=3&utm_source=x&a=1",
            "https://example.com/page?a=1&z=3",
        ),
        # 7. Удаление завершающего слэша у пути
        (
            "https://example.com/page/",
            "https://example.com/page",
        ),
        (
            "https://example.com/page/subpage/",
            "https://example.com/page/subpage",
        ),
        # Корневой путь должен сохранить слэш
        (
            "https://example.com/",
            "https://example.com/",
        ),
        (
            "https://example.com",
            "https://example.com/",
        ),
    ],
)
def test_normalize_common_rules(url, expected):
    assert normalize(url) == expected
