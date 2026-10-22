from src.vectorstore import load_store
from src.chains import answer_question

store = load_store()
answer = answer_question(store, "What does NEP say about online learning?")
print("---- ANSWER ----")
print(answer)
