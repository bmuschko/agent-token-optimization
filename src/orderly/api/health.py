"""Liveness and readiness endpoints."""
from orderly import __version__


class HealthHandler:
    """Reports service health."""

    def __init__(self, checks=None) -> None:
        self.checks = checks or {}

    def live(self) -> dict:
        """Always returns ok when the process is serving."""
        return {"status": "ok", "version": __version__}

    def ready(self) -> dict:
        """Runs every registered readiness check."""
        results = {name: bool(check()) for name, check in self.checks.items()}
        status = "ok" if all(results.values()) else "degraded"
        return {"status": status, "checks": results}
