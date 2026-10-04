"""Date helpers."""
from datetime import datetime, timedelta, timezone

ISO = "%Y-%m-%dT%H:%M:%SZ"


def utc_now() -> datetime:
    """Current time, timezone aware."""
    return datetime.now(timezone.utc)


def to_iso(moment: datetime) -> str:
    """Render a datetime in the format the feeds use."""
    return moment.strftime(ISO)


def parse_iso(text: str) -> datetime:
    """Parse a feed timestamp."""
    return datetime.strptime(text, ISO).replace(tzinfo=timezone.utc)


def days_ago(days: int) -> datetime:
    """A timestamp this many days in the past."""
    return utc_now() - timedelta(days=days)
