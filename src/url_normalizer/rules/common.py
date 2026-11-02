import re
from urllib.parse import parse_qsl, urldefrag, urlencode, urlsplit, urlunsplit

from src.url_normalizer.errors import InvalidURLError

# ===== Validate =====
_DOMAIN_RE = re.compile(
    r"(?:[a-z0-9]+(?:-[a-z0-9]+)*\.)+[a-z]{2,}"  # example.com
    r"|localhost"
    r"|(?:\d{1,3}\.){3}\d{1,3}",  # IPv4
    re.IGNORECASE,
)


def validate_url(url: str) -> None:
    _check_url_is_not_empty(url)
    _check_scheme(url)
    _check_domain(url)


def _check_url_is_not_empty(url: str) -> None:
    if not url:
        raise InvalidURLError("URL is empty")


def _parse(url: str):
    try:
        return urlsplit(url)
    except ValueError as exc:
        raise InvalidURLError(f"Malformed URL: {url!r}") from exc


def _check_scheme(url: str) -> None:
    parsed = _parse(url)
    if parsed.scheme not in ("http", "https"):
        raise InvalidURLError(f"Unsupported scheme: {parsed.scheme!r}")


def _check_domain(url: str) -> None:
    parsed = _parse(url)
    host = parsed.hostname
    if not host or not _DOMAIN_RE.fullmatch(host):
        raise InvalidURLError(f"Invalid domain: {host!r}")


# ===== Apply rules =====
def apply_common_rules(url: str) -> str:
    url = _trim_spaces(url)
    url = _lowercase_scheme_and_host(url)
    url = _normalize_path(url)
    url = _remove_fragment(url)
    url = _remove_trecking_params(url)
    url = _sort_query_params(url)
    return url


def _trim_spaces(url: str) -> str:
    return url.strip(" ")


def _lowercase_scheme_and_host(url: str) -> str:
    parsed = _parse(url)

    userinfo, sep, hostport = parsed.netloc.rpartition("@")
    # remove port
    host, _, _ = hostport.partition(":")

    new_netloc = f"{userinfo}{sep}{host.lower()}"

    new_url = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=new_netloc,
    )
    return urlunsplit(new_url)


def _normalize_path(url: str) -> str:
    parsed = _parse(url)

    if not parsed.path:
        new_path = "/"
    elif len(parsed.path) >= 2:
        new_path = parsed.path.removesuffix("/")
    else:
        new_path = parsed.path

    new_url = parsed._replace(path=new_path)
    return urlunsplit(new_url)


def _remove_fragment(url: str) -> str:
    clean_url, _ = urldefrag(url)

    return clean_url


def _remove_trecking_params(url: str) -> str:
    parsed_url = _parse(url)

    tracking_params = (
        "fbclid",
        "gclid",
        "yclid",
        "mc_cid",
        "mc_eid",
    )

    query_params = parse_qsl(parsed_url.query, keep_blank_values=True)

    filtered_params = [
        (key, value)
        for key, value in query_params
        if not key.lower().startswith("utm_") and key.lower() not in tracking_params
    ]

    new_query = urlencode(filtered_params)

    return urlunsplit(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            new_query,
            parsed_url.fragment,
        )
    )


def _sort_query_params(url: str) -> str:
    parsed_url = _parse(url)

    query_params = parse_qsl(
        parsed_url.query,
        keep_blank_values=True,
    )

    sorted_params = sorted(query_params, key=lambda param: param[0])

    new_query = urlencode(sorted_params)

    return urlunsplit(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            new_query,
            parsed_url.fragment,
        )
    )
