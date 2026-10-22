
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings

# Lightweight embedding model
embeddings = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)


def build_store(chunks, persist_dir="db"):
    # Check whether the PDF produced any chunks
    if not chunks:
        raise ValueError(
            "No text chunks were extracted from the PDF. "
            "Check whether the PDF contains readable text."
        )

    # Remove empty chunks
    valid_chunks = [
        chunk for chunk in chunks
        if chunk.page_content and chunk.page_content.strip()
    ]

    if not valid_chunks:
        raise ValueError(
            "The PDF contains no readable text. "
            "It may be scanned or image-based."
        )

    # Verify that the embedding model produces vectors
    test_embedding = embeddings.embed_documents(
        [valid_chunks[0].page_content]
    )

    if not test_embedding or not test_embedding[0]:
        raise ValueError(
            "The embedding model returned an empty vector."
        )

    return Chroma.from_documents(
        documents=valid_chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )


def load_store(persist_dir="db"):
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )
