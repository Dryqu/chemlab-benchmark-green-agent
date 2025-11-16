import json
import os
from typing import Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REFS_PATH = os.path.join(DATA_DIR, "references.jsonl")


def load_references() -> Dict[str, Dict[str, Any]]:
    refs: Dict[str, Dict[str, Any]] = {}
    with open(REFS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            obj = json.loads(line)
            refs[obj["task_id"]] = obj
    return refs
