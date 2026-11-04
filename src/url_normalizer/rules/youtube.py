from urllib.parse import SplitResult, parse_qs, urlsplit, urlunsplit

from url_normalizer.errors import InvalidURLError


def _parse(url: str) -> SplitResult:
    try:
        return urlsplit(url)
    except ValueError as exc:
        raise InvalidURLError(f"Malformed URL: {url!r}") from exc


def normalize_youtube(url: str) -> str:
    parsed_url = _parse(url)

    id = extract_youtube_id(url)

    if id is None:
        new_parsed_url = parsed_url._replace(scheme="https", netloc="www.youtube.com")
        return urlunsplit(new_parsed_url)

    new_url = f"https://www.youtube.com/watch?v={id}"
    return new_url


def extract_youtube_id(url: str) -> str | None:
    parsed_url = _parse(url)
    path = parsed_url.path
    query = parsed_url.query

    if "v" in parse_qs(query):
        return parse_qs(query)["v"][0]

    if "youtu.be" in parsed_url.netloc:
        return path.lstrip("/")

    path_parts = [part for part in path.split("/") if part]

    if path_parts and path_parts[0] in ["shorts", "embed", "live"]:
        return path_parts[1]

    return None
