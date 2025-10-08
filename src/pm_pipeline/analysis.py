"""Analytical helpers that surface trends for the pipeline."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from statistics import mean
from typing import Dict, Iterable, List, Mapping

from .data_loader import FeedbackDataset, FeedbackRecord
from .preprocess import normalise_text
from .prompt_library import THEMES, Theme


@dataclass
class ThemeSignal:
    theme: Theme
    count: int
    avg_impact: float
    sample_feedback: List[FeedbackRecord]

    @property
    def priority_score(self) -> float:
        return round(self.avg_impact * min(self.count, 5), 2)


@dataclass
class AnalysisResult:
    total_records: int
    segments: Mapping[str, int]
    channels: Mapping[str, int]
    theme_signals: List[ThemeSignal]


def analyse(records: FeedbackDataset) -> AnalysisResult:
    total_records = len(records)
    segments = Counter(record.segment for record in records)
    channels = Counter(record.channel for record in records)

    theme_signals = _theme_signals(records)

    return AnalysisResult(
        total_records=total_records,
        segments=segments,
        channels=channels,
        theme_signals=sorted(theme_signals, key=lambda s: s.priority_score, reverse=True),
    )


def _theme_signals(records: Iterable[FeedbackRecord]) -> List[ThemeSignal]:
    theme_to_feedback: Dict[str, List[FeedbackRecord]] = defaultdict(list)
    for record in records:
        cleaned = normalise_text(record.feedback)
        for theme_id, theme in THEMES.items():
            if any(keyword in cleaned for keyword in theme.keywords):
                theme_to_feedback[theme_id].append(record)

    signals: List[ThemeSignal] = []
    for theme_id, items in theme_to_feedback.items():
        theme = THEMES[theme_id]
        avg_impact = mean(record.impact_weight for record in items)
        signals.append(
            ThemeSignal(
                theme=theme,
                count=len(items),
                avg_impact=round(avg_impact, 2),
                sample_feedback=items[:3],
            )
        )
    return signals


__all__ = ["AnalysisResult", "ThemeSignal", "analyse"]
