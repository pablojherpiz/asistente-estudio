from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from app.ingest import load_pdf, chunk_text

_client = chromadb.PersistentClient(path="data/chroma")
_embed = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)
collection = _client.get_or_create_collection("docs", embedding_function=_embed)


def add_document(path):
    name = Path(path).name
    for page, text in load_pdf(path):
        for i, chunk in enumerate(chunk_text(text)):
            collection.upsert(
                ids=[f"{name}-{page}-{i}"],
                documents=[chunk],
                metadatas=[{"source": name, "page": page}],
            )


def search(question, k=4):
    r = collection.query(query_texts=[question], n_results=k)
    return list(zip(r["documents"][0], r["metadatas"][0]))