import chromadb
import sys
sys.path.append(".")

from backend.read_pdf import read_pdf
from backend.chunker import chunk_text

COLLECTION_NAME = "rag_documents"
_chroma_client = None


def reset_chroma_client():
    global _chroma_client
    _chroma_client = None


def store_chunks(chunks):
    reset_chroma_client()
    client = chromadb.PersistentClient(path="chroma_db")

    try:
        client.delete_collection(COLLECTION_NAME)
    except (ValueError, chromadb.errors.NotFoundError):
        pass

    collection = client.create_collection(name=COLLECTION_NAME)
    collection.add(
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))],
    )

    global _chroma_client
    _chroma_client = client

    print(f"Stored {len(chunks)} chunks in ChromaDB")
    return collection


METADATA_KEYWORDS = (
    "author", "authors", "who wrote", "written by",
    "title", "paper name", "document name",
    "abstract", "affiliation", "university", "institute",
)


def _is_metadata_question(question):
    q = question.lower()
    return any(kw in q for kw in METADATA_KEYWORDS)


def retrieve_chunks(collection, question, n_results=5):
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )
    chunks = list(results["documents"][0])

    # Title-page chunk holds authors/title/abstract; bibliography citations
    # often rank higher for "who are the authors?" in pure semantic search.
    if _is_metadata_question(question):
        title_result = collection.get(ids=["chunk_0"], include=["documents"])
        if title_result["documents"]:
            title_chunk = title_result["documents"][0]
            if title_chunk not in chunks:
                chunks.insert(0, title_chunk)

    return chunks


if __name__ == "__main__":
    # step 1 — read PDF
    print("Reading PDF...")
    raw_text = read_pdf("data/sample.pdf")

    # step 2 — chunk it
    print("Chunking text...")
    chunks = chunk_text(raw_text)

    # step 3 — embed and store
    print("Storing in ChromaDB...")
    collection = store_chunks(chunks)

    # step 4 — test retrieval
    question = "What are the requirements for information security?"
    print(f"\nQuestion: {question}")
    print("----")

    retrieved = retrieve_chunks(collection, question)

    print("Top 3 relevant chunks retrieved:")
    for i, chunk in enumerate(retrieved):
        print(f"\nChunk {i+1}:")
        print(chunk[:300])            # print first 300 chars of each
        print("...")