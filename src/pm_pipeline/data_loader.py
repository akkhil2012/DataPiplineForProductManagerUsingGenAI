"""Utilities for loading product feedback data from CSV sources."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class FeedbackRecord:
    """Normalized representation of a single feedback entry."""

    customer_id: str
    segment: str
    feedback: str
    impact_rating: str
    channel: str
    timestamp: datetime

    @property
    def impact_weight(self) -> int:
        """Map qualitative impact labels to numeric weights."""

        mapping = {
            "critical": 5,
            "high": 4,
            "medium": 3,
            "low": 2,
            "nice to have": 1,
        }
        return mapping.get(self.impact_rating.lower(), 2)


class FeedbackDataset(List[FeedbackRecord]):
    """Simple list-like container with helper constructors."""

    @classmethod
    def from_rows(cls, rows: Iterable[Sequence[str]]) -> "FeedbackDataset":
        items: List[FeedbackRecord] = []
        for row in rows:
            timestamp = _parse_timestamp(row[5])
            record = FeedbackRecord(
                customer_id=row[0].strip(),
                segment=row[1].strip(),
                feedback=row[2].strip(),
                impact_rating=row[3].strip(),
                channel=row[4].strip(),
                timestamp=timestamp,
            )
            items.append(record)
        return cls(items)

    @classmethod
    def from_csv(cls, path: Path) -> "FeedbackDataset":
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            headers = next(reader, None)
            if not headers:
                raise ValueError("CSV file is empty")
            return cls.from_rows(reader)


def _parse_timestamp(raw: str) -> datetime:
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported timestamp format: {raw}")


__all__ = ["FeedbackRecord", "FeedbackDataset"]
