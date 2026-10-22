SUMMARIZE_PROMPT = """You are a senior education policy analyst briefing a university administrator.
Summarize the following policy text. Structure your output as:

## Main Objectives
## Key Reforms
## Benefits
## Important Points to Note

Be factual. Do not add anything not present in the text.

POLICY TEXT:
{text}
"""

RAG_QA_PROMPT = """Answer the question using ONLY the context below.
If the answer is not in the context, say This is not addressed in the provided policy document.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:
"""

COMPARE_PROMPT = """Compare the two education policies below across these dimensions:
Curriculum, Examinations, Technology Integration, Flexibility, Implementation Cost.

Return ONLY a markdown table with columns: Feature | Policy A | Policy B.
Be factual and base the comparison only on the text provided.

POLICY A ({name_a}):
{text_a}

POLICY B ({name_b}):
{text_b}
"""

IMPACT_PROMPT = """You are analyzing the impact of this education policy.
Think step by step:
1. Identify who is affected: students, teachers, universities, government
2. For each stakeholder, reason about direct and indirect effects
3. Then summarize your reasoning into the JSON format below

Question: {question}

POLICY CONTEXT:
{context}

Respond ONLY in this JSON format, with no extra text before or after:
{{
  "students": ["effect 1", "effect 2"],
  "teachers": ["effect 1", "effect 2"],
  "universities": ["effect 1", "effect 2"],
  "government": ["effect 1", "effect 2"]
}}
"""

SIMPLIFY_PROMPT = """Rewrite this policy clause in plain, simple English for a first-year college student.
No jargon. Use short sentences. If a helpful analogy exists, use one.
Keep it under 100 words.

CLAUSE:
{clause}
"""