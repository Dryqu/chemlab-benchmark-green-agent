import random
from typing import Dict, Any, List

from .tasks import load_tasks
from .references import load_references
from .evaluator import ChemLabEvaluator


class ChemLabExpertGreenAgent:
    """
    Green Agent for the ChemLab-Expert benchmark.

    High-level methods:
    - reset(seed)
    - run_single(purple_agent, task_id)
    - run_benchmark(purple_agent, num_tasks)
    """

    def __init__(self, llm_client, seed: int = 42):
        self.seed = seed
        self.tasks: Dict[str, Dict[str, Any]] = load_tasks()
        self.refs: Dict[str, Dict[str, Any]] = load_references()
        self.evaluator = ChemLabEvaluator(llm_client)

    def reset(self, seed: int | None = None) -> None:
        self.seed = seed or self.seed
        random.seed(self.seed)

    def _choose_tasks(self, num_tasks: int) -> List[str]:
        task_ids = list(self.tasks.keys())
        if num_tasks >= len(task_ids):
            return task_ids
        random.seed(self.seed)
        return random.sample(task_ids, num_tasks)

    def run_single(self, purple_agent, task_id: str) -> Dict[str, Any]:
        task = self.tasks[task_id]
        ref = self.refs[task_id]

        agent_report = purple_agent.solve(task)

        result = self.evaluator.score(task, ref, agent_report)

        return {
            "task_id": task_id,
            "score": result["overall"],
            "rubric": result,
            "agent_report": agent_report
        }

    def run_benchmark(self, purple_agent, num_tasks: int = 3) -> Dict[str, Any]:
        chosen = self._choose_tasks(num_tasks)
        results = [self.run_single(purple_agent, tid) for tid in chosen]
        overall = sum(r["score"] for r in results) / len(results)

        return {
            "task_ids": chosen,
            "results": results,
            "overall_score": round(overall, 4)
        }
