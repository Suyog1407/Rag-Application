# RAG Application

A full-stack Retrieval-Augmented Generation (RAG) web application that lets you upload any PDF and ask questions about it. The AI reads your document and answers from it — no hallucinations, no guessing.

![RAG Pipeline](https://img.shields.io/badge/Python-3.11-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-green) ![ChromaDB](https://img.shields.io/badge/ChromaDB-latest-orange) ![Ollama](https://img.shields.io/badge/Ollama-Llama3.2-purple)

---

## How It Works

```
PDF Upload → Text Extraction → Chunking → Embeddings → ChromaDB
                                                            ↓
User Question → Embed Question → Retrieve Relevant Chunks → Llama LLM → Answer
```

**Phase 1 — Ingestion (on upload):**
1. Extract raw text from PDF using PyPDF2
2. Split text into overlapping chunks (500 chars, 50 char overlap)
3. Convert chunks to vector embeddings
4. Store in ChromaDB vector database

**Phase 2 — Query (on every question):**
1. Embed the user's question
2. Find the most semantically similar chunks in ChromaDB
3. Send chunks + question to Llama running locally via Ollama
4. Return the answer with source chunks shown

---

## Features

- Upload any PDF and ask questions about it
- Chat history — all Q&As stay visible, newest on top
- Source highlighting — see exactly which parts of the document the answer came from
- Dark mode toggle with preference saved
- Structured answer formatting for lists and numbered items
- Spinner while answer is generating
- Runs completely offline — no paid APIs, no internet required after setup
- Zero cost to run

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Vector Database | ChromaDB |
| Embeddings | ChromaDB built-in (default) / sentence-transformers (v2) |
| LLM | Llama 3.2 via Ollama (runs locally) |
| PDF Reading | PyPDF2 |

---

## Project Structure

```
rag-application/
├── backend/
│   ├── read_pdf.py          # Extract text from PDF
│   ├── chunker.py           # Split text into chunks
│   ├── embedder_chroma.py   # Store and retrieve chunks (ChromaDB built-in embeddings)
│   └── embedder_st.py       # Store and retrieve chunks (sentence-transformers)
├── templates/
│   └── index.html           # Frontend UI
├── data/                    # Uploaded PDFs stored here
├── app.py                   # Flask server and API routes
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Setup & Installation

### Prerequisites
- Python 3.11
- [Ollama](https://ollama.com) installed and running

### 1. Clone the repository
```bash
git clone https://github.com/Suyog1407/Rag-Application.git
cd Rag-Application
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install and start Ollama
```bash
brew install ollama
brew services start ollama
ollama pull llama3.2
```

### 5. Run the app
```bash
python3 app.py
```

### 6. Open in browser
Go to **http://127.0.0.1:5000**

---

## Usage

1. Click **Choose file** and select any PDF
2. Click **Upload PDF** and wait for processing
3. Type a specific question in the text box
4. Click **Ask** or press Enter
5. Click **▶ Sources** to see which document chunks were used

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serve the frontend |
| POST | `/upload` | Upload and process a PDF |
| POST | `/ask` | Ask a question, returns answer + source chunks |

---

## Key Concepts Demonstrated

- **RAG Pipeline** — chunk → embed → store → retrieve → answer
- **Vector Similarity Search** — semantic search using embeddings, not keywords
- **Prompt Engineering** — structured prompts for consistent LLM output
- **Modular Code Architecture** — each component in a separate file
- **REST API Design** — Flask routes for frontend-backend communication

---

## Author

**Suyog Kshirsagar**
- LinkedIn: [linkedin.com/in/suyog-kshirsagar](https://linkedin.com/in/suyog-kshirsagar)
- GitHub: [github.com/Suyog1407](https://github.com/Suyog1407)
