from functools import lru_cache
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from app.ingest import load_pdf, chunk_text


@lru_cache(maxsize=1)
def get_collection():
    client = chromadb.PersistentClient(path="data/chroma")
    embed = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="paraphrase-multilingual-MiniLM-L12-v2"
    )
    return client.get_or_create_collection("docs", embedding_function=embed)


def add_document(path):
    collection = get_collection()
    name = Path(path).name
    for page, text in load_pdf(path):
        for i, chunk in enumerate(chunk_text(text)):
            collection.upsert(
                ids=[f"{name}-{page}-{i}"],
                documents=[chunk],
                metadatas=[{"source": name, "page": page}],
            )


def search(question, k=4):
    r = get_collection().query(query_texts=[question], n_results=k)
    return list(zip(r["documents"][0], r["metadatas"][0]))

def clear_documents():
    collection = get_collection()
    ids = collection.get()["ids"]
    if ids:
        collection.delete(ids=ids)