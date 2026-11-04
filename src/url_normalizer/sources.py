from enum import StrEnum, auto
from urllib.parse import urlsplit

from url_normalizer.errors import InvalidURLError


class Source(StrEnum):
    GENERIC = auto()
    YOUTUBE = auto()
    REDDIT = auto()


YOUTUBE_DOMAINS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
}

REDDIT_DOMAINS = {
    "reddit.com",
    "www.reddit.com",
    "old.reddit.com",
    "m.reddit.com",
    "redd.it",
}


def _parse_domain(url: str) -> str:
    try:
        parsed = urlsplit(url)
    except ValueError as exc:
        raise InvalidURLError(f"Malformed URL: {url!r}") from exc
    if parsed.hostname is None:
        raise InvalidURLError(f"URL has no host: {url!r}")
    return parsed.hostname


def detect_source(url: str) -> Source:
    domain = _parse_domain(url)
    if domain in YOUTUBE_DOMAINS:
        return Source.YOUTUBE
    if domain in REDDIT_DOMAINS:
        return Source.REDDIT
    return Source.GENERIC
