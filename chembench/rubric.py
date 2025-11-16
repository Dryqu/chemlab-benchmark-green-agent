from typing import Dict


def compute_overall_score(scores: Dict[str, float],
                          weights: Dict[str, float]) -> float:
    total = 0.0
    for k, w in weights.items():
        total += scores.get(k, 0.0) * w
    return round(total, 4)
