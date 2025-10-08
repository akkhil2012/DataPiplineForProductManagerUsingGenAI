"""Generate human-friendly insights from analysis results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

from .analysis import AnalysisResult, ThemeSignal
from .prompt_library import (
    PRODUCT_BRIEF_TEMPLATE,
    ROADMAP_TEMPLATE,
    THEME_SECTION_TEMPLATE,
)


@dataclass
class InsightArtifacts:
    product_brief: str
    roadmap: str
    summary: dict


class HeuristicInsightGenerator:
    """Simple generator that approximates GenAI reasoning."""

    def build_artifacts(self, analysis: AnalysisResult) -> InsightArtifacts:
        brief = self._product_brief(analysis)
        roadmap = self._roadmap(analysis.theme_signals)
        summary = self._summary_payload(analysis)
        return InsightArtifacts(product_brief=brief, roadmap=roadmap, summary=summary)

    def _product_brief(self, analysis: AnalysisResult) -> str:
        top_signal = analysis.theme_signals[0] if analysis.theme_signals else None
        customer_promise = (
            "Deliver a proactive intelligence platform that resolves high impact pain points"
        )
        if top_signal:
            customer_promise = (
                f"Deliver {top_signal.theme.name.lower()} so enterprise teams can {self._first_need(top_signal)}"
            )
        insights = self._insight_bullets(analysis.theme_signals)
        evidence = self._evidence_summary(analysis)
        stakeholders = "design, data science, and compliance"
        return PRODUCT_BRIEF_TEMPLATE.format(
            customer_promise=customer_promise,
            insight_bullets=insights,
            evidence_summary=evidence,
            stakeholders=stakeholders,
        )

    def _insight_bullets(self, theme_signals: Sequence[ThemeSignal]) -> str:
        lines = []
        for signal in theme_signals[:3]:
            sample = signal.sample_feedback[0].feedback if signal.sample_feedback else ""
            lines.append(
                f"- **{signal.theme.name}**: {sample} (signal strength {signal.priority_score}/5)"
            )
        if not lines:
            lines.append("- Customer feedback volume is currently low; gather more inputs.")
        return "\n".join(lines)

    def _evidence_summary(self, analysis: AnalysisResult) -> str:
        dominant_segment = max(analysis.segments, key=analysis.segments.get, default="all segments")
        dominant_channel = max(analysis.channels, key=analysis.channels.get, default="mixed channels")
        return f"{analysis.total_records} records across {dominant_segment} via {dominant_channel}"

    def _first_need(self, signal: ThemeSignal) -> str:
        if not signal.sample_feedback:
            return "solve emergent needs"
        return signal.sample_feedback[0].feedback.lower()

    def _roadmap(self, theme_signals: Iterable[ThemeSignal]) -> str:
        sections: List[str] = []
        for signal in theme_signals:
            sections.append(
                THEME_SECTION_TEMPLATE.format(
                    theme_name=signal.theme.name,
                    why_now=self._why_now(signal),
                    signal_strength=round(signal.priority_score, 1),
                    first_experiment=self._experiment(signal),
                )
            )
        if not sections:
            sections.append("No roadmap items identified. Collect additional feedback.")
        return ROADMAP_TEMPLATE.format(theme_sections="\n\n".join(sections))

    def _why_now(self, signal: ThemeSignal) -> str:
        if signal.avg_impact >= 4:
            return "High impact enterprise accounts cite this as a blocker"
        if signal.count > 3:
            return "Volume of requests indicates a near-term retention risk"
        return "Emerging opportunity to differentiate vs competitors"

    def _experiment(self, signal: ThemeSignal) -> str:
        if signal.theme.name.startswith("Trust"):
            return "Partner with security to ship audit logging beta"
        if signal.theme.name.startswith("Workflow"):
            return "Launch AI guided onboarding pilot"
        if signal.theme.name.startswith("Analytics"):
            return "Prototype predictive forecasting dashboards"
        return "Run performance benchmarking sprint"

    def _summary_payload(self, analysis: AnalysisResult) -> dict:
        return {
            "total_records": analysis.total_records,
            "segments": dict(analysis.segments),
            "channels": dict(analysis.channels),
            "themes": [
                {
                    "name": signal.theme.name,
                    "count": signal.count,
                    "avg_impact": signal.avg_impact,
                    "priority_score": signal.priority_score,
                }
                for signal in analysis.theme_signals
            ],
        }


__all__ = ["HeuristicInsightGenerator", "InsightArtifacts"]
