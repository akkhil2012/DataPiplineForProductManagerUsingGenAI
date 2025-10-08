from __future__ import annotations

import json
from io import StringIO
import csv
from pathlib import Path

from pm_pipeline.data_loader import FeedbackDataset
from pm_pipeline.pipeline import Pipeline


def build_dataset() -> FeedbackDataset:
    csv_content = StringIO(
        "customer_id,segment,feedback,impact_rating,channel,timestamp\n"
        "C1,Enterprise,Need better analytics dashboards,High,Interview,2024-01-01\n"
        "C2,Enterprise,Need better analytics dashboards,High,Interview,2024-01-02\n"
        "C3,SMB,Executives request predictive analytics forecasts,High,Brief,2024-01-10\n"
        "C4,SMB,Security audit reports missing,Critical,RFP,2024-02-10\n"
        "C5,SMB,Automation templates would accelerate onboarding,Medium,Survey,2024-02-14\n"
    )
    csv_content.seek(0)
    reader = csv.reader(csv_content)
    next(reader)  # skip header
    return FeedbackDataset.from_rows(reader)


def test_pipeline_generates_artifacts(tmp_path: Path) -> None:
    dataset = build_dataset()
    pipeline = Pipeline()
    result = pipeline.run(dataset)

    assert result.analysis.total_records == 4  # duplicates removed
    assert result.analysis.theme_signals[0].theme.name == "Analytics Intelligence"

    output_dir = tmp_path / "outputs"
    Pipeline.write_outputs(result, output_dir)

    brief = (output_dir / "product_brief.md").read_text(encoding="utf-8")
    roadmap = (output_dir / "roadmap.md").read_text(encoding="utf-8")
    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))

    assert "Product Opportunity Brief" in brief
    assert "Roadmap Recommendations" in roadmap
    assert summary["total_records"] == 4
    assert summary["themes"][0]["name"] == "Analytics Intelligence"
