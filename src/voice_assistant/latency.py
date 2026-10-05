import time
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class LatencyEntry:
    stage: str
    started_at: datetime
    ended_at: datetime
    duration_ms: float
    success: bool
    details: str = ""


class LatencyLogger:
    """Receptor de métricas de latencia por etapa."""

    def __init__(self) -> None:
        self.entries: list[LatencyEntry] = []

    def record(self, stage: str, started_at: datetime, ended_at: datetime, success: bool, details: str = "") -> None:
        duration_ms = (ended_at - started_at).total_seconds() * 1000
        self.entries.append(
            LatencyEntry(
                stage=stage,
                started_at=started_at,
                ended_at=ended_at,
                duration_ms=duration_ms,
                success=success,
                details=details,
            )
        )

    def mark(self, stage: str, *, success: bool = True, details: str = "") -> tuple[datetime, callable]:
        started_at = datetime.now(timezone.utc)

        def finalize() -> LatencyEntry:
            ended_at = datetime.now(timezone.utc)
            self.record(stage, started_at, ended_at, success, details)
            return self.entries[-1]

        return started_at, finalize

    def summary(self) -> dict[str, float]:
        summary: dict[str, float] = {}
        for entry in self.entries:
            stage = entry.stage
            summary[stage] = summary.get(stage, 0.0) + entry.duration_ms
        return summary
