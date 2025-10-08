# Data Pipeline for Product Managers Using GenAI

This repository provides a lightweight product insights pipeline inspired by the
prompt described in [DataPiplineForProductManagerUsingGenAI](https://github.com/akkhil2012/DataPiplineForProductManagerUsingGenAI).

The goal of the application is to help product managers transform raw customer
feedback into structured, actionable artifacts using a GenAI-inspired approach.
Since access to remote LLM services is unavailable in this execution
environment, the project ships with a transparent heuristic generator that
emulates GenAI behaviour. The pipeline is modular, so it can be replaced with a
real LLM-backed implementation when desired.

## Features

- **Data ingestion**: Load customer feedback from CSV files into strongly typed
  data classes.
- **Pre-processing**: Cleanse and normalise feedback text, remove noise, and
  detect duplicates.
- **Theme detection**: Classify feedback into strategic product themes with
  configurable keyword dictionaries.
- **Impact scoring**: Combine qualitative impact assessments with occurrence
  frequency to surface high priority opportunities.
- **Insight generation**: Produce product briefs, customer journey summaries,
  and roadmap recommendations using templated reasoning similar to GenAI
  outputs.
- **CLI utility**: Run the complete pipeline and export summaries as Markdown
  files ready for inclusion in product review documents.

## Project Structure

```
.
├── data
│   └── sample_feedback.csv      # Example dataset used by the tests and demo
├── src
│   └── pm_pipeline
│       ├── __init__.py
│       ├── analysis.py          # Theme extraction & scoring logic
│       ├── cli.py               # Command line interface entrypoint
│       ├── data_loader.py       # CSV ingestion helpers
│       ├── insight_generator.py # Heuristic "GenAI" output generator
│       ├── pipeline.py          # Orchestration of the full workflow
│       ├── preprocess.py        # Text normalisation utilities
│       └── prompt_library.py    # Prompt templates & keyword dictionaries
└── tests
    └── test_pipeline.py         # Automated regression tests
```

## Quickstart

Create a virtual environment and install dependencies (only the standard
library is used, so this step is optional):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # optional: empty placeholder for future deps
```

Run the pipeline on the bundled sample data:

```bash
python -m pm_pipeline.cli --input data/sample_feedback.csv --output build
```

The command writes generated insights to the `build/` directory. Files include:

- `product_brief.md`: top opportunities and customer promise.
- `roadmap.md`: recommended roadmap themes and priority scores.
- `summary.json`: structured export of aggregated metrics.

## Testing

Automated tests validate the core analytics logic:

```bash
pytest
```

## Extending With Real GenAI Services

To plug in a live LLM provider, implement a drop-in replacement for
`insight_generator.HeuristicInsightGenerator` that delegates the prompt
construction to `prompt_library` and sends requests to the provider of your
choice. The rest of the pipeline can remain unchanged.

## License

This project is released under the MIT License.
