# 📄 PDF RAG Application

An AI-powered **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask questions based entirely on the uploaded document's content.

The application extracts and chunks PDF text using **LlamaIndex**, generates semantic embeddings using **Voyage AI**, stores vectors in **Qdrant**, retrieves relevant document chunks through semantic similarity search, and generates context-aware answers using **Groq's GPT-OSS-120B** model.

The backend is built with **FastAPI**, while **Inngest** is used to orchestrate event-driven workflows, execution logs, retries, throttling, and rate limiting. The frontend is built using **Streamlit**.

---

## Features

* Upload PDF documents for indexing
* Parse and chunk PDFs using LlamaIndex
* Generate semantic embeddings using Voyage AI
* Store embeddings in Qdrant Vector Database
* Retrieve relevant document chunks using vector similarity search
* Generate context-aware answers using Groq GPT-OSS-120B
* Ground LLM responses using retrieved document context
* Event-driven backend powered by Inngest
* Automatic workflow retries
* Workflow execution logs through Inngest Dev Server
* Throttling and rate limiting for PDF ingestion
* Local persistent Qdrant storage

---

# Architecture

```text
                           ┌──────────────┐
                           │     User     │
                           └──────┬───────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Streamlit    │
                         │    Frontend     │
                         └────────┬────────┘
                                  │
                             HTTP Request
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         │   + Inngest     │
                         └────────┬────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
                  ▼                               ▼
        ┌──────────────────┐            ┌──────────────────┐
        │ rag/ingest_pdf   │            │ rag/query_pdf_ai │
        └────────┬─────────┘            └────────┬─────────┘
                 │                               │
                 ▼                               ▼
        ┌──────────────────┐            ┌──────────────────┐
        │ Load & Chunk PDF │            │ Embed Question   │
        │   LlamaIndex     │            │    Voyage AI     │
        └────────┬─────────┘            └────────┬─────────┘
                 │                               │
                 ▼                               ▼
        ┌──────────────────┐            ┌──────────────────┐
        │ Voyage AI        │            │ Qdrant           │
        │ Embeddings       │            │ Vector Search    │
        └────────┬─────────┘            └────────┬─────────┘
                 │                               │
                 ▼                               ▼
        ┌──────────────────┐            ┌──────────────────┐
        │ Qdrant           │            │ Retrieve Top-K   │
        │ Vector Database  │            │ Context Chunks   │
        └────────┬─────────┘            └────────┬─────────┘
                 │                               │
                 └───────────────┬───────────────┘
                                 │
                                 ▼
                         ┌─────────────────┐
                         │ Groq GPT-OSS    │
                         │     120B        │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │  Grounded      │
                         │    Answer      │
                         └─────────────────┘
```

---

# RAG Workflow

## 1. PDF Upload & Ingestion

When a user uploads a PDF:

1. Streamlit accepts the uploaded PDF.
2. An Inngest event `rag/ingest_pdf` is triggered.
3. LlamaIndex parses the PDF.
4. The extracted text is divided into smaller chunks.
5. Voyage AI generates embeddings for each chunk.
6. The embeddings and metadata are stored in Qdrant.

```text
PDF
 │
 ▼
LlamaIndex
 │
 ▼
Text Extraction
 │
 ▼
Chunking
 │
 ▼
Voyage AI Embeddings
 │
 ▼
Qdrant
```

---

## 2. Question Answering

When a user asks a question:

1. Streamlit sends the question to the backend.
2. The `rag/query_pdf_ai` Inngest event is triggered.
3. Voyage AI converts the question into an embedding.
4. Qdrant performs semantic similarity search.
5. The Top-K relevant chunks are retrieved.
6. The retrieved chunks are combined into a context block.
7. Groq GPT-OSS-120B receives the context and question.
8. The model generates an answer grounded in the retrieved information.

```text
User Question
      │
      ▼
Voyage AI Embedding
      │
      ▼
Qdrant Similarity Search
      │
      ▼
Top-K Relevant Chunks
      │
      ▼
Context + Question
      │
      ▼
Groq GPT-OSS-120B
      │
      ▼
Final Answer
```

---

# Tech Stack

| Category        | Technology        |
| --------------- | ----------------- |
| Frontend        | Streamlit         |
| Backend         | FastAPI           |
| Workflow Engine | Inngest           |
| PDF Parsing     | LlamaIndex        |
| Embeddings      | Voyage AI         |
| LLM             | Groq GPT-OSS-120B |
| Vector Database | Qdrant            |
| Language        | Python 3.12       |
| Package Manager | UV                |
| API Server      | Uvicorn           |
| Configuration   | python-dotenv     |
| Data Validation | Pydantic          |

---

# Project Structure

```text
pdf-rag-application/
│
├── uploads/                 # Uploaded PDF documents
├── qdrant_storage/          # Local Qdrant database storage
├── .venv/                   # Python virtual environment
│
├── main.py                  # FastAPI application + Inngest workflows
├── streamlit_app.py         # Streamlit frontend
├── data_loader.py           # PDF parsing, chunking & embeddings
├── vector_db.py             # Qdrant search and upsert operations
├── custom_types.py          # Pydantic request/response models
├── reset_qdrant.py          # Reset Qdrant collection
│
├── .env.example             # Environment variable template
├── pyproject.toml            # Project configuration & dependencies
├── uv.lock                   # Locked dependencies
└── README.md                 # Project documentation
```

---

# API Endpoints

FastAPI hosts the application, while the actual business logic is executed through **Inngest event functions**.

## Ingest PDF

### Endpoint

```http
POST /rag/ingest_pdf
```

### Triggered Event

```text
rag/ingest_pdf
```

### Purpose

Indexes a PDF document into the Qdrant vector database.

### Request Body

```json
{
  "data": {
    "pdf_path": "uploads/robotics_notes.pdf"
  }
}
```

### Processing Steps

| Inngest Step       | Description                                                        |
| ------------------ | ------------------------------------------------------------------ |
| `load-and-chunk`   | Loads the PDF and splits the document into chunks using LlamaIndex |
| `embed-and-upsert` | Generates Voyage AI embeddings and stores them in Qdrant           |

### Example Response

```json
{
  "ingested": 84
}
```

---

# Query PDF

### Endpoint

```http
POST /rag/query_pdf_ai
```

### Triggered Event

```text
rag/query_pdf_ai
```

### Purpose

Answers questions using information retrieved from indexed PDF documents.

### Request Body

```json
{
  "data": {
    "question": "Explain hydraulic actuating systems.",
    "top_k": 5
  }
}
```

### Processing Steps

| Inngest Step       | Description                                                        |
| ------------------ | ------------------------------------------------------------------ |
| `embed-and-search` | Embeds the question and retrieves Top-K similar chunks from Qdrant |
| `llm-answer`       | Generates the final answer using Groq GPT-OSS-120B                 |

### Example Response

```json
{
  "answer": "Hydraulic actuating systems use pressurized fluid to generate motion...",
  "sources": [
    "robotics_notes.pdf"
  ],
  "num_contexts": 5
}
```

---

# AI Models

## Voyage AI — Embeddings

Voyage AI is used to generate dense vector embeddings for:

* PDF document chunks
* User questions

The embeddings allow the system to compare the semantic meaning of the question with the semantic meaning of document chunks.

```text
PDF Chunk ──────► Embedding Vector
                       │
                       ▼
                    Qdrant


User Question ──► Embedding Vector
                       │
                       ▼
                 Similarity Search
```

---

## Groq GPT-OSS-120B — Generation

Groq's **GPT-OSS-120B** is used for the final answer generation.

The model receives:

```text
Retrieved Context
       +
User Question
       │
       ▼
GPT-OSS-120B
       │
       ▼
Grounded Answer
```

A system prompt instructs the model to answer using the provided context, helping reduce hallucinations and keep responses grounded in the uploaded documents.

---

# Environment Variables

Create a `.env` file in the project root.

```env
VOYAGE_API_KEY=your_voyage_api_key
GROQ_API_KEY=your_groq_api_key
```

---

# Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/harshakuchi/pdf-rag-application.git

cd pdf-rag-application
```

---

## 2. Install Dependencies

This project uses **UV** for Python dependency management.

```bash
uv sync
```

---

## 3. Activate the Virtual Environment

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
VOYAGE_API_KEY=your_voyage_api_key
GROQ_API_KEY=your_groq_api_key
```

---

## 5. Start Qdrant

Run Qdrant locally using Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Qdrant will be available at:

```text
http://localhost:6333
```

---

## 6. Start Inngest Development Server

Run:

```bash
npx inngest-cli@latest dev
```

The Inngest development dashboard will be available at:

```text
http://localhost:8288
```

---

## 7. Start the FastAPI Backend

```bash
uv run uvicorn main:app --reload
```

Backend:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

## 8. Start the Streamlit Frontend

Open another terminal and run:

```bash
uv run streamlit run streamlit_app.py
```

Frontend:

```text
http://localhost:8501
```

---

# Complete Request Flow

The complete application flow can be summarized as:

```text
                         PDF INGESTION
                              │
                              ▼
                        Streamlit Upload
                              │
                              ▼
                      FastAPI / Inngest
                              │
                              ▼
                         Parse PDF
                              │
                              ▼
                          Chunk Text
                              │
                              ▼
                     Voyage AI Embedding
                              │
                              ▼
                           Qdrant
                              │
                              │
                              ▼
                       Indexed Document


                         QUESTION ANSWERING
                              │
                              ▼
                       User Question
                              │
                              ▼
                      Voyage AI Embedding
                              │
                              ▼
                   Qdrant Similarity Search
                              │
                              ▼
                       Top-K Chunks
                              │
                              ▼
                     Context + Question
                              │
                              ▼
                       Groq GPT-OSS-120B
                              │
                              ▼
                         Final Answer
```

---

# Dependencies

The major dependencies used by the project include:

```text
fastapi
streamlit
inngest
llama-index
qdrant-client
voyageai
groq
uvicorn
python-dotenv
pydantic
```

Install everything using:

```bash
uv sync
```

---
