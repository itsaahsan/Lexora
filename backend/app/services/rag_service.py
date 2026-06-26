import os
import json
import numpy as np
import faiss
import google.generativeai as genai
from app.config import get_settings
from app.schemas.chat import Source

settings = get_settings()

_configured = False


def _ensure_configured():
    global _configured
    if not _configured:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _configured = True


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
            _index = faiss.IndexFlatL2(768)
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
    _ensure_configured()
    result = genai.embed_content(
        model=settings.GEMINI_EMBEDDING_MODEL,
        content=texts,
        task_type="retrieval_document",
    )
    return result["embedding"]


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

    query_embedding = get_embeddings([query])
    query_vector = np.array(query_embedding, dtype=np.float32)
    distances, indices = index.search(query_vector, min(k, index.ntotal))

    results = []
    for dist, idx in zip(distances[0], indices[0]):
        if idx < len(_metadata_map):
            meta = _metadata_map[idx]
            results.append({
                "text": meta.get("text", ""),
                "document_id": meta.get("document_id", ""),
                "chunk_index": meta.get("chunk_index", 0),
                "score": float(1 / (1 + dist)),
            })

    return results


def generate_answer(query: str, context_chunks: list[dict]) -> str:
    _ensure_configured()
    context = "\n\n".join([
        f"[Document {i+1}]: {chunk['text']}"
        for i, chunk in enumerate(context_chunks)
    ])

    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    response = model.generate_content(
        f"""You are Lexora, an AI assistant for document Q&A.
Answer questions based on the provided document context.
If the context doesn't contain enough information, say so.
Always cite which document(s) you used.

Context:
{context}

Question: {query}""",
        generation_config=genai.GenerationConfig(
            temperature=0.3,
            max_output_tokens=1000,
        ),
    )
    return response.text


def retrieve_and_generate(query: str, user_id: str) -> dict:
    results = search_similar(query, k=5, user_id=user_id)
    answer = generate_answer(query, results)

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
