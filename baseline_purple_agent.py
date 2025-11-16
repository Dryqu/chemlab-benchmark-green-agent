class BaselinePurpleAgent:
    """
    A very simple baseline purple agent for debugging the benchmark.
    It just calls an LLM with the task description and returns a markdown report.
    """

    def __init__(self, llm_client):
        self.llm = llm_client

    def solve(self, task):
        prompt = f"""
You are a research assistant in analytical chemistry.

Goal:
{task["goal"]}

Requirements:
{task["requirements"]}

Please return a structured scientific report in Markdown with:
- Introduction
- Main analysis (methods / reasoning)
- Comparison table or troubleshooting tree if required
- Recommendation or conclusion

Be concise but complete. Do not mention that you are an AI model.
"""
        return self.llm.chat(system_prompt="", user_prompt=prompt)
