from src.ingest import load_and_chunk
from src.chains import compare_policies

nep = load_and_chunk("data/policies/NEP_2020.pdf")
ugc = load_and_chunk("data/policies/ugc_regulations.pdf")
print("NEP chunks:", len(nep), "| UGC chunks:", len(ugc))

text_a = " ".join(c.page_content for c in nep[40:50])
text_b = " ".join(c.page_content for c in ugc[10:20])

result = compare_policies("NEP 2020", text_a, "UGC Regulations", text_b)
print("---- COMPARISON ----")
print(result)
