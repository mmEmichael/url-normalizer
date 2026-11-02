from src.url_normalizer.rules.common import apply_common_rules, validate_url


def normalize(url: str) -> str:
    validate_url(url)
    url = apply_common_rules(url)
    return url
