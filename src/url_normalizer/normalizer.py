from src.url_normalizer.rules.common import apply_common_rules, validate_url
from src.url_normalizer.sources import Source, detect_source
from url_normalizer.rules.reddit import extract_reddit_id, normalize_reddit
from url_normalizer.rules.youtube import extract_youtube_id, normalize_youtube


def normalize(url: str) -> str:
    validate_url(url)
    url = apply_common_rules(url)

    if detect_source(url) == Source.YOUTUBE:
        url = normalize_youtube(url)
    if detect_source(url) == Source.REDDIT:
        url = normalize_reddit(url)

    return url


def extract_id(url: str) -> str | None:
    if detect_source(url) == Source.YOUTUBE:
        return extract_youtube_id(url)
    if detect_source(url) == Source.REDDIT:
        return extract_reddit_id(url)
