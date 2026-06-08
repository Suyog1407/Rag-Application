import chromadb
import sys
sys.path.append(".")

from sentence_transformers import SentenceTransformer
from backend.read_pdf import read_pdf
from backend.chunker import chunk_text

# load the embedding model (downloads once, cached after)
model = SentenceTransformer("all-MiniLM-L6-v2")


def store_chunks(chunks):
    client = chromadb.PersistentClient(path="chroma_db_st")

    collection = client.get_or_create_collection(name="rag_documents_st")

    for i, chunk in enumerate(chunks):
        # THIS is what ChromaDB was doing silently in Version 1
        # you are now doing it yourself manually
        embedding = model.encode(chunk).tolist()   # text → numbers

        collection.add(
            documents=[chunk],          # original text
            embeddings=[embedding],     # YOU are providing the numbers
            ids=[f"chunk_{i}"]
        )

    print(f"Stored {len(chunks)} chunks with manual embeddings")
    return collection


def retrieve_chunks(collection, question, n_results=3):
    # embed the question yourself too
    question_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[question_embedding],   # YOU provide the vector
        n_results=n_results
    )
    return results["documents"][0]


if __name__ == "__main__":
    print("Reading PDF...")
    raw_text = read_pdf("data/sample.pdf")

    print("Chunking text...")
    chunks = chunk_text(raw_text)

    print("Generating embeddings and storing...")
    collection = store_chunks(chunks)

    question = "What are the requirements for information security?"
    print(f"\nQuestion: {question}")
    print("----")

    retrieved = retrieve_chunks(collection, question)

    print("Top 3 relevant chunks retrieved:")
    for i, chunk in enumerate(retrieved):
        print(f"\nChunk {i+1}:")
        print(chunk[:300])
        print("...")