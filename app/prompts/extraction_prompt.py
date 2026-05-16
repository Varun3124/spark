def build_extraction_prompt(user_query: str):
    return f"""
You are an information extraction system for a corporate research platform.

Your task is to extract structured intelligence from natural language research queries.

Rules:
- Return ONLY valid JSON
- Do not include markdown
- If information is missing, use null
- Do not hallucinate values

Query:
{user_query}
"""


