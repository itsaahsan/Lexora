import os
from app.utils.file_parser import parse_file
from app.utils.chunker import chunk_text
from app.services.rag_service import add_documents_to_index


def process_document(document_id: str, file_path: str, file_type: str, user_id: str = None) -> int:
    text = parse_file(file_path, file_type)
    if not text:
        return 0

    chunks = chunk_text(text)
    if not chunks:
        return 0

    metadatas = [
        {"document_id": document_id, "chunk_index": i, "user_id": str(user_id) if user_id else ""}
        for i in range(len(chunks))
    ]

    add_documents_to_index(document_id, chunks, metadatas)
    return len(chunks)
