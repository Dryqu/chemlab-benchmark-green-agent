# ChemLab-Expert Benchmark (Green Agent)

A Research Agent Benchmark for Analytical Chemistry  
**Phase 1 – AgentX / AgentBeats Competition (UC Berkeley)**  
**Target analyte:** Atrazine (pesticide)

## Overview

ChemLab-Expert is a Green Agent benchmark designed to evaluate the scientific research capabilities of Purple Agents in analytical chemistry. The benchmark focuses on real-world tasks involving atrazine method development, literature search, chromatographic evaluation, troubleshooting, and structured scientific summarization.

The Green Agent:

* Provides analytical chemistry tasks
* Receives structured reports from a Purple Agent
* Scores them using a rubric-based evaluator
* Returns deterministic, reproducible results

## Task Types

The benchmark contains tasks in five categories:

1. Literature extraction \& summarization
2. HPLC/LC-MS method comparison
3. Troubleshooting reasoning
4. Sample preparation \& recovery inference
5. Technical reporting summarization

Atrazine is the primary analyte for all tasks in Phase 1.

## Artifact Submission Pattern

Each Purple Agent submits one artifact:

* A structured scientific report in Markdown
* Containing specific sections required by each task
* The Green Agent evaluates the artifact using the rubric \& reference keys

## Scoring

Each task is graded using five criteria (0–5):

* Task completion
* Factual correctness
* Coverage
* Clarity \& structure
* Format compliance

Weighted average → overall score (0–5).  
The benchmark returns:

* Per-task scores
* Rubric breakdown
* Optional evaluator comments
* Final averaged score

## Reproducibility Rules

* All tasks and reference data are static files in `data/`
* Deterministic sampling using seeded RNG
* LLM evaluator runs at temperature 0
* Fixed prompts and scoring templates

## How to Run the Benchmark

This repository provides a Green Agent (“ChemLab-Expert”) that evaluates Purple Agents on analytical chemistry research tasks involving atrazine.

### 1\. Install dependencies

This package currently has no heavy dependencies. Create a virtual environment and install the project:

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\\Scripts\\activate
pip install .
```

### 2\. Prepare an LLM client

Example (pseudo):

```python
class MyLLM:
    def chat(self, system\_prompt, user\_prompt):
        from openai import OpenAI
        client = OpenAI()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=\[
                {"role": "system", "content": system\_prompt},
                {"role": "user", "content": user\_prompt}
            ],
            temperature=0
        )
        return resp.choices\[0].message\["content"]
```

### 3\. Create a Purple Agent

Use the simple baseline agent included:

```python
from baseline\_purple\_agent import BaselinePurpleAgent
purple = BaselinePurpleAgent(MyLLM())
```

### 4\. Run the Green Agent

```python
from chembench.green\_agent import ChemLabExpertGreenAgent

green = ChemLabExpertGreenAgent(MyLLM(), seed=42)
green.reset()

result = green.run\_benchmark(purple\_agent=purple, num\_tasks=3)
print(result)
```

### 5\. Output Format

The benchmark returns:

* Selected task IDs
* Each task’s rubric scores
* The Purple Agent’s report
* The final averaged score (0–5)

This completes a reproducible evaluation run of the ChemLab-Expert benchmark.



## File Structure

```
chemlab-benchmark-green-agent/
  README.md
  pyproject.toml
  data/
    tasks.jsonl
    references.jsonl
  chembench/
    \_\_init\_\_.py
    tasks.py
    references.py
    rubric.py
    evaluator.py
    green\_agent.py
  baseline\_purple\_agent.py
```

## License

Open benchmark released for AgentX / AgentBeats 2025 Phase 1.

