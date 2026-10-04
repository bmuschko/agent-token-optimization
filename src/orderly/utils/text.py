"""String helpers."""
import re

_SLUG = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    """Lowercase a string and replace runs of non-alphanumerics with dashes."""
    return _SLUG.sub("-", value.lower()).strip("-")


def truncate(value: str, limit: int, suffix: str = "...") -> str:
    """Shorten a string to a limit, appending a suffix when it was cut."""
    if len(value) <= limit:
        return value
    return value[: max(0, limit - len(suffix))] + suffix


def mask(value: str, keep: int = 4) -> str:
    """Mask all but the trailing characters of a sensitive value."""
    if len(value) <= keep:
        return "*" * len(value)
    return "*" * (len(value) - keep) + value[-keep:]
