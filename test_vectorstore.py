from src.ingest import load_and_chunk
from src.vectorstore import build_store

chunks = load_and_chunk("data/policies/NEP_2020.pdf")
print("Chunks loaded:", len(chunks))

print("Building vector store... this may take a minute the first time (downloading embedding model)")
store = build_store(chunks)
print("Vector store built and saved to ./db")

results = store.similarity_search("What does NEP say about online learning?", k=3)
print("---- Top matching chunk ----")
print(results[0].page_content)
