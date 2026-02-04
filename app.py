# ---------- Imports ----------
import streamlit as st
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# ---------- Embedding model ----------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_model()

def get_embedding(text):
    return embedding_model.encode(text).tolist()

# ---------- MongoDB ----------
client_db = MongoClient("MONGO_URI")
collection = client_db["rag_db"]["test"]

# ---------- Retrieval ----------
def get_query_results(query):
    query_embedding = get_embedding(query)

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 380,
                "limit": 10
            }
        },
        {
            "$project": {
                "_id": 0,
                "text": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]

    results = list(collection.aggregate(pipeline))

    # Remove duplicates
    seen = set()
    unique = []
    for r in results:
        if r["text"] not in seen:
            unique.append(r)
            seen.add(r["text"])

    return unique[:5]

# ---------- UI ----------
st.title("📚 MongoDB Semantic Search Demo")

query = st.text_input("Ask a question:")

if st.button("Search"):
    results = get_query_results(query)

    # threshold check
    if not results or results[0]["score"] < 0.65:
        st.warning("No relevant information found in the document.")
    else:
        st.subheader("Top Results:")
        for r in results:
            st.write(f"Score: {r['score']:.3f}")
            st.write(r["text"])
            st.write("Secret loaded:", bool(st.secrets.get("MONGO_URI")))
            st.divider()

