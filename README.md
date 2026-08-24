# 📄 PDF RAG Application

An AI-powered **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask questions based solely on their contents.

The application extracts text from PDFs, converts them into vector embeddings using **Voyage AI**, stores them in **Qdrant Vector Database**, retrieves the most relevant chunks using semantic search, and generates grounded answers using **Groq LLMs** through **LlamaIndex**. The backend APIs are built with **FastAPI**, orchestrated using **Inngest**, and the user interface is developed with **Streamlit**.

---

## Project Architecture

```text
                    User
                      │
                      ▼
              Streamlit Frontend
                      │
          HTTP Requests (REST APIs)
                      │
                      ▼
                FastAPI Backend
                      │
          ┌───────────┴────────────┐
          │                        │
          ▼                        ▼
   PDF Ingestion API         Query API
          │                        │
          ▼                        ▼
     LlamaIndex Parser       Retrieve Context
          │                        │
          ▼                        ▼
 Voyage AI Embeddings      Qdrant Vector Search
          │                        │
          └───────────┬────────────┘
                      ▼
               Groq LLM Generation
                      │
                      ▼
              Response to User
```

---

#  How RAG Works in this Project

This application follows a complete **Retrieval-Augmented Generation pipeline**.

### Step 1 — Upload PDF

The user uploads a PDF through the Streamlit interface.

### Step 2 — Parse PDF

LlamaIndex reads and extracts text from the PDF while preserving document structure.

### Step 3 — Chunking

The extracted text is divided into smaller chunks so relevant information can be retrieved efficiently.

### Step 4 — Embedding Generation

Each chunk is converted into a high-dimensional vector using **Voyage AI Embedding Model**.

### Step 5 — Store in Qdrant

Embeddings along with metadata are stored inside **Qdrant**, which acts as the vector database.

### Step 6 — Ask a Question

The user asks a natural language question.

### Step 7 — Semantic Retrieval

The question is embedded using Voyage AI and Qdrant retrieves the most similar document chunks.

### Step 8 — LLM Response

The retrieved chunks are passed as context to a **Groq-hosted LLM** which generates an answer grounded in the uploaded document.

---

## Tech Stack

| Category               | Technology          |
| ---------------------- | ------------------- |
| Frontend               | Streamlit           |
| Backend                | FastAPI             |
| API Orchestration      | Inngest             |
| PDF Parsing            | LlamaIndex          |
| Embeddings             | Voyage AI           |
| LLM                    | Groq (Llama Models) |
| Vector Database        | Qdrant              |
| Environment Management | UV + Python 3.12    |

---

## Project Structure

```text
pdf-rag-application/
│
├── uploads/                 # Uploaded PDF files
├── qdrant_storage/          # Local Qdrant vector storage
├── .venv/                   # Virtual environment
│
├── main.py                  # FastAPI application
├── streamlit_app.py         # Streamlit frontend
├── data_loader.py           # PDF loading & chunking
├── vector_db.py             # Qdrant operations
├── custom_types.py          # Shared request/response models
├── reset_qdrant.py          # Utility to clear vector database
│
├── .env.example             # Environment variables template
├── pyproject.toml           # Project dependencies
├── uv.lock                  # UV lock file
└── README.md
```

---

# API Endpoints

The backend exposes two primary endpoints.

## 1. Upload & Index PDF

**Endpoint**

```http
POST /rag/ingest_pdf
```

Uploads a PDF, parses it using LlamaIndex, generates embeddings, and stores vectors inside Qdrant.

### Request

```json
{
  "data": {
      "pdf_path": "path"
  }
}
```

---

## 2. Ask Questions from PDF

**Endpoint**

```http
POST /rag/query_pdf_ai
```

Accepts a user query, retrieves relevant document chunks, and returns an AI-generated answer.

### Request

```json
{
  "data": {
      "question": "question"
  }
}
```

---

# Why Inngest?

This project uses **Inngest** during local development to orchestrate API workflows.

### Benefits

* Event-driven execution.
* Tracks every endpoint execution.
* Provides detailed logs for debugging.
* Makes long-running ingestion workflows easier to monitor.
* Simplifies asynchronous processing.

For every API invocation, Inngest records execution status, timing, and logs.

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/harshakuchi/pdf-rag-application.git

cd pdf-rag-application
```

## 2. Install Dependencies

Using **uv**

```bash
uv sync
```

Activate virtual environment.

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

---

## 3. Configure Environment Variables

Create a `.env` file.

```env
VOYAGE_API_KEY=your_voyage_api_key

GROQ_API_KEY=your_groq_api_key
```

---

## 4. Start Qdrant

Using Docker

```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

## 5. Start Inngest Dev Server (Prerequisite: Node.js)

```bash
npx inngest-cli@latest dev
```

The development dashboard will show endpoint executions and logs.

---

## 6. Run FastAPI Backend

```bash
uv run uvicorn main:app
```

---

## 7. Run Streamlit Frontend

```bash
uv run streamlit run .\streamlit_app.py
```

---

# Dependencies

Major libraries used in this project include:

```text
fastapi
streamlit
llama-index
qdrant-client
voyageai
groq
inngest
uvicorn
python-dotenv
```
