"""Text pre-processing utilities."""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable, List

from .data_loader import FeedbackDataset, FeedbackRecord


_SANITIZE_RE = re.compile(r"[^a-z0-9\s]")


def normalise_text(text: str) -> str:
    """Lowercase text and remove punctuation."""

    lowered = text.lower().strip()
    normalised = _SANITIZE_RE.sub("", lowered)
    return re.sub(r"\s+", " ", normalised)


def deduplicate(records: FeedbackDataset) -> FeedbackDataset:
    """Remove duplicate feedback entries based on the cleaned text."""

    seen = set()
    unique: List[FeedbackRecord] = []
    for record in records:
        cleaned = normalise_text(record.feedback)
        if cleaned in seen:
            continue
        seen.add(cleaned)
        unique.append(record)
    return FeedbackDataset(unique)


def keyword_counts(records: Iterable[FeedbackRecord], keywords: Iterable[str]) -> Counter:
    """Count keyword occurrences across all feedback entries."""

    counts: Counter = Counter()
    keyword_set = {normalise_text(word) for word in keywords}
    for record in records:
        cleaned = normalise_text(record.feedback)
        for keyword in keyword_set:
            if keyword in cleaned:
                counts[keyword] += 1
    return counts


__all__ = ["normalise_text", "deduplicate", "keyword_counts"]
