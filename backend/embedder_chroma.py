import chromadb
import sys
sys.path.append(".")

from backend.read_pdf import read_pdf
from backend.chunker import chunk_text

def store_chunks(chunks):
    # create a local ChromaDB client (saves data in a folder called chroma_db)
    client = chromadb.PersistentClient(path="chroma_db")

    # create a collection — think of it like a table in a database
    collection = client.get_or_create_collection(name="rag_documents")

    # store each chunk with a unique ID
    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],        # the actual text
            ids=[f"chunk_{i}"]        # unique ID for each chunk
        )

    print(f"Stored {len(chunks)} chunks in ChromaDB")
    return collection


def retrieve_chunks(collection, question, n_results=3):
    results = collection.query(
        query_texts=[question],       # your question in plain text
        n_results=n_results           # how many chunks to retrieve
    )
    return results["documents"][0]    # returns list of matching chunks


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