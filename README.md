# RAG Application

A full-stack Retrieval-Augmented Generation (RAG) web application that lets you upload any PDF and ask questions about it. The AI reads your document and answers from it.

## How It Works

PDF Upload → Text Extraction → Chunking → Embeddings → ChromaDB → Retrieval → Llama LLM → Answer

## Features

- Upload any PDF and ask questions about it
- Chat history with newest answers on top
- Source highlighting — see which document chunks were used
- Dark mode toggle
- Structured answer formatting
- Runs completely offline — no paid APIs, zero cost

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- Vector Database: ChromaDB
- LLM: Llama 3.2 via Ollama (runs locally)
- PDF Reading: PyPDF2

## Setup

1. Clone the repo
2. Create virtual environment: python3 -m venv venv
3. Activate: source venv/bin/activate
4. Install: pip install -r requirements.txt
5. Install Ollama and pull model: ollama pull llama3.2
6. Run: python3 app.py
7. Open: http://127.0.0.1:5000

## Author

Suyog Kshirsagar
- LinkedIn: https://linkedin.com/in/suyog-kshirsagar
- GitHub: https://github.com/Suyog1407
