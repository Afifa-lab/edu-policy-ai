import json
from groq import Groq
from dotenv import load_dotenv
from src.prompts import (
    SUMMARIZE_PROMPT, RAG_QA_PROMPT, COMPARE_PROMPT,
    IMPACT_PROMPT, SIMPLIFY_PROMPT
)

load_dotenv()
client = Groq()

def call_llm(prompt, max_tokens=2000):
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

def summarize_policy(text):
    return call_llm(SUMMARIZE_PROMPT.format(text=text[:12000]))

def answer_question(vectorstore, question, k=4):
    docs = vectorstore.similarity_search(question, k=k)
    context = "\n\n".join(d.page_content for d in docs)
    return call_llm(RAG_QA_PROMPT.format(context=context, question=question))

def compare_policies(name_a, text_a, name_b, text_b):
    return call_llm(COMPARE_PROMPT.format(
        name_a=name_a, text_a=text_a[:6000],
        name_b=name_b, text_b=text_b[:6000]
    ))

def analyze_impact(vectorstore, question, k=5):
    docs = vectorstore.similarity_search(question, k=k)
    context = "\n\n".join(d.page_content for d in docs)
    raw = call_llm(IMPACT_PROMPT.format(context=context, question=question))
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"raw": raw}

def simplify_clause(clause):
    return call_llm(SIMPLIFY_PROMPT.format(clause=clause))
