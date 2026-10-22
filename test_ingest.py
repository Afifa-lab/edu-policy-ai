from src.ingest import load_and_chunk

chunks = load_and_chunk("data/policies/NEP_2020.pdf")
print("Number of chunks:", len(chunks))
print("---- First chunk content ----")
print(chunks[0].page_content)
