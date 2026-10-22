from src.ingest import load_and_chunk
from src.chains import summarize_policy

chunks = load_and_chunk("data/policies/NEP_2020.pdf")
full_text = " ".join(c.page_content for c in chunks[10:30])
print("---- SUMMARY ----")
print(summarize_policy(full_text))
