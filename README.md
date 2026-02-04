# MongoDB RAG Semantic Search

A Retrieval-Augmented Generation (RAG) style semantic search system built using local embeddings and MongoDB Atlas vector search. The application allows users to query a document and retrieve the most semantically relevant text chunks using cosine similarity.(add ip addrees from site)

This project demonstrates an end-to-end vector retrieval pipeline suitable for production-style AI systems.

---

## Features

- Local embeddings using SentenceTransformers (no paid APIs)
- MongoDB Atlas vector indexing
- Semantic similarity search
- Ranked retrieval with similarity scores
- Duplicate chunk filtering
- Streamlit UI for interactive querying
- Fully offline retrieval pipeline

---

## Architecture

User Query  
→ SentenceTransformer Embedding  
→ MongoDB Vector Search  
→ Ranked Semantic Retrieval  
→ UI Display

This project focuses on the retrieval stage of a RAG pipeline.

---

## Tech Stack

- Python
- Streamlit
- MongoDB Atlas Vector Search
- SentenceTransformers
- PyMongo
- LangChain utilities (document loading & splitting)

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/mongodb-rag-demo.git
cd mongodb-rag-demo
```

Create virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Mac/Linux
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
streamlit run app.py
```

The browser UI will open automatically.

---

## MongoDB Setup

1. Create a MongoDB Atlas cluster
2. Enable Vector Search
3. Insert embedded document chunks
4. Create vector index with 384 dimensions
5. Allow network access (0.0.0.0/0 for development)

---

## How It Works

1. PDF is loaded and split into semantic chunks
2. Each chunk is embedded using SentenceTransformers
3. Embeddings are stored in MongoDB
4. User query is embedded
5. MongoDB returns top cosine similarity matches
6. Results are ranked and deduplicated
7. UI displays relevant context

---

## Example Output

Similarity Score: 0.734  
Top matching semantic document chunk is returned to the user.

Scores closer to 1.0 indicate stronger semantic similarity.

---

## Why This Project Matters

This project demonstrates:

- Vector database engineering
- Embedding pipelines
- Semantic retrieval systems
- Practical RAG architecture
- Production-style AI system design

It can be extended into a full RAG assistant by adding a local or cloud LLM for answer generation.

---

## Future Improvements

- Local LLM integration (offline RAG)
- Chat interface with memory
- PDF upload ingestion from UI
- Reranking pipeline
- Docker deployment
- Cloud hosting
- Streaming responses

---

## License

MIT License
