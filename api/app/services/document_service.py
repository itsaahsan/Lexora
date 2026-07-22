import logging
from app.utils.file_parser import parse_file
from app.utils.chunker import chunk_text
from app.services.rag_service import add_documents_to_index

logger = logging.getLogger(__name__)


def process_document(document_id: str, file_path: str, file_type: str, user_id: str = None) -> int:
    try:
        text = parse_file(file_path, file_type)
        if not text:
            logger.warning(f"No text extracted from {file_path}")
            return 0

        chunks = chunk_text(text)
        if not chunks:
            logger.warning(f"No chunks generated from {file_path}")
            return 0

        metadatas = [
            {"document_id": document_id, "chunk_index": i, "user_id": str(user_id) if user_id else ""}
            for i in range(len(chunks))
        ]

        add_documents_to_index(document_id, chunks, metadatas)
        return len(chunks)
    except Exception as e:
        logger.error(f"Document processing error: {e}")
        return 0
