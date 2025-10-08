"""Prompt templates and semantic theme definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Theme:
    """Represents a strategic product theme."""

    name: str
    description: str
    keywords: List[str]


THEMES: Dict[str, Theme] = {
    "analytics": Theme(
        name="Analytics Intelligence",
        description="Advanced analytics, forecasting, and AI-driven insights",
        keywords=[
            "analytics",
            "dashboard",
            "forecast",
            "predictive",
            "insight",
            "chart",
            "cohort",
        ],
    ),
    "automation": Theme(
        name="Workflow Automation",
        description="Automation templates, AI assistants, onboarding guidance",
        keywords=[
            "automation",
            "workflow",
            "guided",
            "tour",
            "template",
            "ai",
        ],
    ),
    "compliance": Theme(
        name="Trust & Compliance",
        description="Security, audit readiness, and enterprise governance",
        keywords=[
            "security",
            "audit",
            "soc2",
            "compliance",
            "fraud",
            "log",
        ],
    ),
    "scale": Theme(
        name="Scalability",
        description="Performance, exports, bulk workflows, and reliability",
        keywords=[
            "export",
            "bulk",
            "performance",
            "scalability",
            "load",
            "latency",
        ],
    ),
}


PRODUCT_BRIEF_TEMPLATE = """# Product Opportunity Brief

## Customer Promise
{customer_promise}

## High Impact Insights
{insight_bullets}

## Confidence & Next Steps
- Confidence is boosted by {evidence_summary}.
- Recommend engaging {stakeholders} to scope discovery workshops.
"""


ROADMAP_TEMPLATE = """# Roadmap Recommendations

{theme_sections}
"""


THEME_SECTION_TEMPLATE = """## {theme_name}
- Why now: {why_now}
- Signal strength: {signal_strength}/5
- First experiment: {first_experiment}
"""


__all__ = [
    "Theme",
    "THEMES",
    "PRODUCT_BRIEF_TEMPLATE",
    "ROADMAP_TEMPLATE",
    "THEME_SECTION_TEMPLATE",
]
