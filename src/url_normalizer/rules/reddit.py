from urllib.parse import urlsplit, urlunsplit

from url_normalizer.errors import InvalidURLError


def _parse(url: str):
    try:
        return urlsplit(url)
    except ValueError as exc:
        raise InvalidURLError(f"Malformed URL: {url!r}") from exc


def _split_path(path: str) -> list:
    return [part for part in path.split("/") if part]


def normalize_reddit(url: str) -> str:
    parsed_url = _parse(url)

    if "redd.it" in parsed_url.netloc:
        return url

    path = parsed_url.path
    path_parts = _split_path(path)

    id = extract_reddit_id(url)

    if id is None:
        new_parsed_url = parsed_url._replace(scheme="https", netloc="www.reddit.com")
        return urlunsplit(new_parsed_url)

    comments_index = path_parts.index("r")
    sub_reddit = path_parts[comments_index + 1]

    new_url = f"https://www.reddit.com/r/{sub_reddit}/comments/{id}/"
    return new_url


def extract_reddit_id(url: str):
    parsed_url = _parse(url)
    path = parsed_url.path

    path_parts = _split_path(path)

    if "redd.it" in parsed_url.netloc:
        return path.lstrip("/")

    if "comments" in path_parts:
        comments_index = path_parts.index("comments")
        return path_parts[comments_index + 1]

    return None
