import json
from typing import Dict, Any
from .rubric import compute_overall_score

EVALUATOR_SYSTEM_PROMPT = """
You are an analytical chemistry evaluator specializing in HPLC and LC-MS environmental analysis.
You will receive:
1) The task description,
2) The reference key points,
3) The agent's submitted report.

Your job is to strictly evaluate the agent's report using the rubric below.

Rubric (each 0–5):
- task_completion: Did the report follow ALL required instructions?
- factual_correctness: Are statements chemically and chromatographically correct?
- coverage: Does it cover REQUIRED items (methods, parameters, tables, etc.)?
- clarity_structure: Is the report organized, readable, and logically structured?
- format_compliance: Does it match the required sections, output format, or tables?

Return ONLY a JSON dictionary:
{
  "task_completion": <0–5>, 
  "factual_correctness": <0–5>,
  "coverage": <0–5>,
  "clarity_structure": <0–5>,
  "format_compliance": <0–5>,
  "overall": <weighted_average>,
  "comments": "Short evaluator comments"
}

Do not include explanations outside the JSON.
""".strip()


class ChemLabEvaluator:
    def __init__(self, llm_client):
        """
        llm_client: a thin wrapper, e.g.
        llm_client.chat(system_prompt, user_prompt) -> str
        """
        self.llm = llm_client

    def _build_user_prompt(
        self,
        task: Dict[str, Any],
        ref: Dict[str, Any],
        agent_report: str
    ) -> str:
        return f"""
TASK:
{json.dumps(task, indent=2, ensure_ascii=False)}

REFERENCE KEY POINTS:
{json.dumps(ref.get("key_points", []), indent=2, ensure_ascii=False)}

MUST-NOT VIOLATIONS:
{json.dumps(ref.get("must_not", []), indent=2, ensure_ascii=False)}

AGENT REPORT:
{agent_report}
""".strip()

    def score(
        self,
        task: Dict[str, Any],
        ref: Dict[str, Any],
        agent_report: str
    ) -> Dict[str, Any]:
        user_prompt = self._build_user_prompt(task, ref, agent_report)

        raw = self.llm.chat(
            system_prompt=EVALUATOR_SYSTEM_PROMPT,
            user_prompt=user_prompt
        )

        try:
            scores = json.loads(raw)
        except json.JSONDecodeError:
            scores = {
                "task_completion": 0.0,
                "factual_correctness": 0.0,
                "coverage": 0.0,
                "clarity_structure": 0.0,
                "format_compliance": 0.0,
                "comments": "Failed to parse evaluator response as JSON."
            }

        weights = ref.get("rubric_weights", {
            "task_completion": 0.2,
            "factual_correctness": 0.3,
            "coverage": 0.2,
            "clarity_structure": 0.2,
            "format_compliance": 0.1
        })

        scores["overall"] = compute_overall_score(scores, weights)
        return scores
