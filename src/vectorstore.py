from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

# Light embedding model (runs on ONNX, no PyTorch needed)
embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")


def build_store(chunks, persist_dir="db"):
    return Chroma.from_documents(chunks, embeddings, persist_directory=persist_dir)


def load_store(persist_dir="db"):
    return Chroma(persist_directory=persist_dir, embedding_function=embeddings)