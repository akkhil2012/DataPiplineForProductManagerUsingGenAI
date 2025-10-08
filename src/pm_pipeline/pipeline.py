"""High-level orchestration for the product insights pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .analysis import AnalysisResult, analyse
from .data_loader import FeedbackDataset
from .insight_generator import HeuristicInsightGenerator, InsightArtifacts
from .preprocess import deduplicate


@dataclass
class PipelineResult:
    analysis: AnalysisResult
    artifacts: InsightArtifacts


class Pipeline:
    """Execute the end-to-end workflow from CSV to insight artifacts."""

    def __init__(self, generator: Optional[HeuristicInsightGenerator] = None) -> None:
        self._generator = generator or HeuristicInsightGenerator()

    def run(self, dataset: FeedbackDataset) -> PipelineResult:
        unique = deduplicate(dataset)
        analysis = analyse(unique)
        artifacts = self._generator.build_artifacts(analysis)
        return PipelineResult(analysis=analysis, artifacts=artifacts)

    def run_from_csv(self, path: Path) -> PipelineResult:
        dataset = FeedbackDataset.from_csv(path)
        return self.run(dataset)

    @staticmethod
    def write_outputs(result: PipelineResult, output_dir: Path) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "product_brief.md").write_text(result.artifacts.product_brief, encoding="utf-8")
        (output_dir / "roadmap.md").write_text(result.artifacts.roadmap, encoding="utf-8")
        (output_dir / "summary.json").write_text(
            json.dumps(result.artifacts.summary, indent=2, default=str),
            encoding="utf-8",
        )


__all__ = ["Pipeline", "PipelineResult"]
