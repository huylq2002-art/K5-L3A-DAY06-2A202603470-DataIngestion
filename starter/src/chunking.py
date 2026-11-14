"""Implement fixed-size and structure-aware chunking."""
import uuid
from .models import Chunk, DocumentPage


def _make_chunk(page: DocumentPage, text: str, chunk_index: int) -> Chunk:
    """Helper to create a Chunk from a DocumentPage and text slice."""
    chunk_id = f"{page.document_id}_p{page.page:03d}_c{chunk_index:03d}"
    metadata = dict(page.metadata)  # copy page-level metadata
    metadata["chunk_index"] = chunk_index
    return Chunk(
        chunk_id=chunk_id,
        document_id=page.document_id,
        source=page.source,
        page=page.page,
        text=text.strip(),
        metadata=metadata,
    )


def fixed_size(page: DocumentPage, size: int, overlap: int) -> list[Chunk]:
    """Split text into overlapping character windows and retain page metadata.
    
    Strategy A: Fixed-size chunking with character-level sliding window.
    - size: target chunk size in characters
    - overlap: number of characters to overlap between adjacent chunks
    """
    text = page.text
    if not text:
        return []

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = min(start + size, len(text))
        chunk_text = text[start:end]

        if len(chunk_text.strip()) > 20:  # skip near-empty slices
            chunks.append(_make_chunk(page, chunk_text, chunk_index))
            chunk_index += 1

        if end >= len(text):
            break
        start += (size - overlap)

    return chunks


def by_paragraph(page: DocumentPage, max_size: int) -> list[Chunk]:
    """Group paragraphs, split oversized paragraphs, and retain metadata.
    
    Strategy B/C: Structure-aware chunking that respects paragraph boundaries.
    - max_size: maximum characters per chunk before splitting
    - Paragraphs are separated by blank lines or numbered list items (Điều X, digit.)
    """
    text = page.text
    if not text:
        return []

    # Split on blank lines or Vietnamese numbered list patterns
    import re
    # Split on double newlines (paragraph boundaries)
    raw_paragraphs = re.split(r'\n{2,}', text)

    # Further split on numbered items like "1.", "2.", "- " at line start
    paragraphs = []
    for para in raw_paragraphs:
        sub_paras = re.split(r'\n(?=\d+\.|[-•]\s)', para)
        paragraphs.extend(sub_paras)

    chunks = []
    chunk_index = 0
    current_text = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # If adding this paragraph would exceed max_size, flush current buffer
        if current_text and (len(current_text) + len(para) + 2) > max_size:
            if len(current_text.strip()) > 20:
                chunks.append(_make_chunk(page, current_text, chunk_index))
                chunk_index += 1
            current_text = para
        else:
            current_text = (current_text + "\n" + para).strip() if current_text else para

        # If a single paragraph is itself larger than max_size, split it
        if len(current_text) > max_size:
            # Split by sentences or at max_size boundary
            while len(current_text) > max_size:
                split_at = current_text.rfind('. ', 0, max_size)
                if split_at == -1 or split_at < max_size // 2:
                    split_at = max_size
                chunk_text = current_text[:split_at + 1].strip()
                if len(chunk_text) > 20:
                    chunks.append(_make_chunk(page, chunk_text, chunk_index))
                    chunk_index += 1
                current_text = current_text[split_at + 1:].strip()

    # Flush remaining buffer
    if current_text.strip() and len(current_text.strip()) > 20:
        chunks.append(_make_chunk(page, current_text, chunk_index))

    return chunks
