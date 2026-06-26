import os
import json
import numpy as np
import faiss
from google import genai
from google.genai import types
from app.config import get_settings
from app.schemas.chat import Source

settings = get_settings()

EMBEDDING_DIM = 3072

_client = None


def _ensure_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)


_index = None
_id_map = []
_metadata_map = []


def _get_index():
    global _index
    if _index is None:
        index_path = os.path.join(settings.FAISS_INDEX_PATH, "index.faiss")
        if os.path.exists(index_path):
            _index = faiss.read_index(index_path)
            _load_metadata()
        else:
            os.makedirs(settings.FAISS_INDEX_PATH, exist_ok=True)
            _index = faiss.IndexFlatL2(EMBEDDING_DIM)
    return _index


def _load_metadata():
    global _id_map, _metadata_map
    meta_path = os.path.join(settings.FAISS_INDEX_PATH, "metadata.json")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            data = json.load(f)
            _id_map = data.get("ids", [])
            _metadata_map = data.get("metadatas", [])


def _save_metadata():
    meta_path = os.path.join(settings.FAISS_INDEX_PATH, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump({"ids": _id_map, "metadatas": _metadata_map}, f)


def _save_index():
    index_path = os.path.join(settings.FAISS_INDEX_PATH, "index.faiss")
    faiss.write_index(_index, index_path)
    _save_metadata()


def get_embeddings(texts: list[str]) -> list[list[float]]:
    _ensure_client()
    result = _client.models.embed_content(
        model=settings.GEMINI_EMBEDDING_MODEL,
        contents=texts,
    )
    return [e.values for e in result.embeddings]


def get_query_embedding(text: str) -> list[float]:
    _ensure_client()
    result = _client.models.embed_content(
        model=settings.GEMINI_EMBEDDING_MODEL,
        contents=[text],
    )
    return result.embeddings[0].values


def add_documents_to_index(document_id: str, chunks: list[str], metadatas: list[dict]):
    index = _get_index()
    embeddings = get_embeddings(chunks)
    vectors = np.array(embeddings, dtype=np.float32)
    index.add(vectors)

    for i, chunk in enumerate(chunks):
        _id_map.append(f"{document_id}_chunk_{i}")
        _metadata_map.append({
            **metadatas[i],
            "text": chunk,
        })

    _save_index()


def search_similar(query: str, k: int = 5, user_id: str = None) -> list[dict]:
    index = _get_index()
    if index.ntotal == 0:
        return []

    query_embedding = get_query_embedding(query)
    query_vector = np.array([query_embedding], dtype=np.float32)

    search_k = min(k * 3, index.ntotal)
    distances, indices = index.search(query_vector, search_k)

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx >= 0 and idx < len(_metadata_map):
            meta = _metadata_map[idx]
            if user_id and meta.get("user_id") and meta["user_id"] != str(user_id):
                continue
            results.append({
                "text": meta.get("text", ""),
                "document_id": meta.get("document_id", ""),
                "chunk_index": meta.get("chunk_index", 0),
                "score": float(1 / (1 + dist)),
            })
            if len(results) >= k:
                break

    return results


def generate_answer(query: str, context_chunks: list[dict]) -> str:
    _ensure_client()

    if context_chunks:
        context = "\n\n".join([
            f"[Document {i+1}]: {chunk['text']}"
            for i, chunk in enumerate(context_chunks)
        ])
        prompt = f"""You are Lexora, an AI assistant for document Q&A.
Answer questions based on the provided document context.
If the context doesn't contain enough information, say so.
Always cite which document(s) you used.

Context:
{context}

Question: {query}"""
    else:
        prompt = f"""You are Lexora, an AI assistant for document Q&A.
No relevant documents were found. Answer the question using your general knowledge, and mention that no documents were matched.

Question: {query}"""

    response = _client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=1000,
        ),
    )
    return response.text


def retrieve_and_generate(query: str, user_id: str) -> dict:
    results = search_similar(query, k=5, user_id=user_id)

    try:
        answer = generate_answer(query, results)
    except Exception:
        if results:
            answer = "I found relevant documents but couldn't generate an answer right now. Please try again later.\n\n"
            answer += "Matched content:\n"
            for i, r in enumerate(results, 1):
                answer += f"\n[{i}] {r['text'][:200]}"
        else:
            answer = "I couldn't process your request right now. The AI service is temporarily unavailable. Please try again later."

    sources = [
        Source(
            document_id=r["document_id"],
            filename="",
            chunk_text=r["text"],
            score=r["score"],
        )
        for r in results
    ]

    return {"answer": answer, "sources": sources}
