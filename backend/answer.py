import ollama
import sys
sys.path.append(".")

from backend.read_pdf import read_pdf
from backend.chunker import chunk_text
from backend.embedder_chroma import store_chunks, retrieve_chunks


def generate_answer(question, retrieved_chunks):
    # build the prompt — this is exactly what gets sent to the LLM
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't know based on the document."

Context:
{context}

Question: {question}

Answer:"""

    # send to Ollama running locally
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    # step 1 — read and chunk
    print("Reading PDF...")
    raw_text = read_pdf("data/sample.pdf")
    chunks = chunk_text(raw_text)

    # step 2 — store in ChromaDB
    print("Storing chunks...")
    collection = store_chunks(chunks)

    # step 3 — ask a question
    question = "What should top management do for information security leadership?"
    print(f"\nQuestion: {question}")
    print("----")

    # step 4 — retrieve relevant chunks
    retrieved = retrieve_chunks(collection, question)

    # step 5 — generate answer
    print("Generating answer...")
    answer = generate_answer(question, retrieved)

    print("\nAnswer:")
    print(answer)