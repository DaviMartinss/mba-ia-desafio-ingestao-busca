# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Document RAG (Retrieval-Augmented Generation) system** that ingests PDF documents, generates embeddings, stores them in a vector database, and enables intelligent querying through a chat interface.

**Pipeline:** PDF → Chunking → Embeddings → PostgreSQL+pgvector → Vector Search → LLM Response

## Tech Stack

- **Language:** Python 3.10+
- **LLM Framework:** LangChain (0.3.27) with LangChain Community, Core, and Google GenAI components
- **Vector Database:** PostgreSQL with pgvector extension (pgvector/pgvector:pg17)
- **Embedding Model:** Google Generative AI (gemini-embedding-001)
- **Chat Model:** Google GenerativeAI (gemini-2.5-flash)
- **PDF Processing:** PyPDF
- **Text Splitting:** LangChain RecursiveCharacterTextSplitter
- **Configuration:** python-dotenv for environment variables

## Project Structure

```
.
├── src/
│   ├── ingest.py       # PDF loader, chunking, embedding generation & storage
│   ├── chat.py         # Interactive chat interface with vector search
│   └── search.py       # Vector search utilities & prompt templates
├── docker-compose.yml  # PostgreSQL + pgvector setup
├── requirements.txt    # Python dependencies
├── .env               # Environment config (create this)
└── document.pdf       # Target PDF (user-provided)
```

## Common Development Commands

### Setup & Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Database
```bash
# Start PostgreSQL with pgvector
docker compose up -d

# Check service health
docker ps

# Stop services
docker compose down

# View logs
docker compose logs postgres

# Clean data volumes
docker compose down -v
```

### Core Operations
```bash
# Ingest a PDF and generate embeddings
python src/ingest.py

# Start interactive chat with the ingested document
python src/chat.py
```

## Architecture & Key Concepts

### Ingestion Pipeline (ingest.py)
1. **PDF Loading:** Uses PyPDFLoader to read PDF from `PDF_PATH`
2. **Chunking:** RecursiveCharacterTextSplitter divides text into overlapping chunks (1000 tokens, 150-token overlap)
3. **Embedding Generation:** Google Generative AI embeddings model converts text to vectors
4. **Batch Processing:** Documents processed in batches of 5 with 2-second delays to respect API rate limits (RPM/TPM)
5. **Vector Storage:** PGVector stores chunks with embeddings in PostgreSQL using JSONB for metadata

### Chat & Retrieval (chat.py)
1. **Vector Search:** Similarity search retrieves top-10 most relevant chunks for user query
2. **Context Aggregation:** Search results passed as context to LLM
3. **Response Generation:** Chat model generates responses grounded in retrieved context
4. **Temperature:** Set to 0 for deterministic responses

### Search Utilities (search.py)
- Prompt templates for context-aware querying
- Integration layer between vector store and LLM chain

## Environment Configuration

Create a `.env` file in the project root with:

```env
# Google API for embeddings and chat
GOOGLE_API_KEY=your_google_api_key_here

# PostgreSQL connection (default for docker-compose setup)
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5434/rag

# Vector store collection name
PG_VECTOR_COLLECTION_NAME=desafio01

# Path to PDF file (absolute or relative)
PDF_PATH=document.pdf
```

**Obtain credentials:**
- Google API Key: https://ai.google.dev/ → Get API Key

## Rate Limiting & Batching

The ingestion pipeline respects rate limits through:
- Batch size of 5 documents
- 2-second delay between batches
- Document ID generation to prevent duplicates

If you encounter quota errors, increase batch delays or reduce batch size in `ingest.py` line 51-67.

## Key Dependencies & Versions

- `langchain`: 0.3.27 (core framework)
- `langchain-google-genai`: 2.1.9 (embedding & chat models)
- `langchain-postgres`: 0.0.15 (vector store with pgvector)
- `pypdf`: 6.0.0 (PDF parsing)
- `psycopg-binary`: 3.2.9 (PostgreSQL driver)

## Common Issues & Troubleshooting

### Database Connection Refused
- Verify PostgreSQL container is running: `docker ps`
- Restart services: `docker compose down && docker compose up -d`

### No module named 'langchain'
- Check venv is activated (should see `(venv)` in terminal)
- Reinstall: `pip install -r requirements.txt`

### PDF_PATH not set or file not found
- Verify `.env` exists in project root
- Use absolute path or place PDF in project root
- Check file permissions

### API quota/rate limit errors
- Increase batch delays in `ingest.py`
- Reduce chunk overlap or token size
- Space out ingestion jobs

### Connection refused on localhost:5434
- Docker daemon might not be running
- Check Docker Desktop is open (Windows/macOS)
- Use `docker-compose logs` to debug startup
