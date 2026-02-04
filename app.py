# ---------- Imports ----------
import streamlit as st
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

st.title("📚 MongoDB Semantic Search Demo")

# ---------- Check secret ----------
if "MONGO_URI" not in st.secrets:
    st.error("MongoDB secret not found. Add MONGO_URI in Streamlit secrets.")
    st.stop()

uri = st.secrets["MONGO_URI"]

# ---------- MongoDB connection ----------
try:
    client_db = MongoClient(
        uri,
        tls=True,
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000
    )
    client_db.server_info()  # force connection test
    collection = client_db["rag_db"]["test"]
except Exception as e:
    st.error("Failed to connect to MongoDB")
    st.write(e)
    st.stop()

# ---------- Embedding model ----------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

embedding_model = load_model()

def get_embedding(text):
    return embedding_model.encode(text).tolist()

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
query = st.text_input("Ask a question:")

if st.button("Search") and query:
    try:
        results = get_query_results(query)

        if not results or results[0]["score"] < 0.65:
            st.warning("No relevant information found in the document.")
        else:
            st.subheader("Top Results:")
            for r in results:
                st.write(f"Score: {r['score']:.3f}")
                st.write(r["text"])
                st.divider()

    except Exception as e:
        st.error("Search failed")
        st.write(e)
