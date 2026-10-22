from src.vectorstore import load_store
from src.chains import analyze_impact

store = load_store()
result = analyze_impact(store, "How does this policy affect engineering and higher education students?")
print("---- IMPACT ANALYSIS ----")
print(result)
