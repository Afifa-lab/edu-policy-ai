from src.ingest import load_and_chunk
from src.vectorstore import build_store, load_store
from src.chains import compare_policies

ugc_chunks = load_and_chunk("data/policies/ugc_regulations.pdf")
ugc_store = build_store(ugc_chunks, persist_dir="db_ugc")
nep_store = load_store()

query = "curriculum, examinations and assessment, technology and online learning, flexibility, funding and cost"
text_a = "\n\n".join(d.page_content for d in nep_store.similarity_search(query, k=6))
text_b = "\n\n".join(d.page_content for d in ugc_store.similarity_search(query, k=6))

print("---- COMPARISON ----")
print(compare_policies("NEP 2020", text_a, "UGC Regulations 2018", text_b))
