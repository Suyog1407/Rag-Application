from flask import Flask, request, jsonify, render_template
import os
import sys
import shutil
sys.path.append(".")

from backend.read_pdf import read_pdf
from backend.chunker import chunk_text
from backend.embedder_chroma import store_chunks, retrieve_chunks
import ollama

app = Flask(__name__)
UPLOAD_FOLDER = "data"

collection = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    global collection

    file = request.files["pdf"]
    file_path = os.path.join(UPLOAD_FOLDER, "uploaded.pdf")
    file.save(file_path)

    # delete old vector database so old chunks don't mix with new ones
    if os.path.exists("chroma_db"):
        shutil.rmtree("chroma_db")

    raw_text = read_pdf(file_path)
    chunks = chunk_text(raw_text)
    collection = store_chunks(chunks)

    return jsonify({"message": f"PDF uploaded. {len(chunks)} chunks created."})


@app.route("/ask", methods=["POST"])
def ask():
    global collection

    if collection is None:
        return jsonify({"answer": "Please upload a PDF first."})

    data = request.get_json()
    question = data["question"]

    retrieved = retrieve_chunks(collection, question)
    context = "\n\n".join(retrieved)

    prompt = f"""You are an expert document analyst. A user has uploaded a document and wants detailed answers.

Use the context below to answer thoroughly. Include specific numbers, facts, and details from the document.
If multiple pieces of context are relevant, combine them into a complete answer.
If the answer is not in the context, say "This information is not in the document."

When listing items, always use this exact format:
1. [First item]
2. [Second item]
3. [Third item]

Context from document:
{context}

Question: {question}

Provide a detailed, accurate answer:"""

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({
        "answer": response["message"]["content"],
        "sources": retrieved
    })


if __name__ == "__main__":
    app.run(debug=True)