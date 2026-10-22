from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk(pdf_path):
    docs = PyPDFLoader(pdf_path).load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800, chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)
    print("Document loaded:", len(doc))
    print("Chunks, created:", len(chunks))
    return chunks
