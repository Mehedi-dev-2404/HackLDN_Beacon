import re


def chunk_text(
    text: str,
    max_chunk_size: int = 1000,
    overlap: int = 100,
) -> list[str]:
    if max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= max_chunk_size:
        raise ValueError("overlap must be smaller than max_chunk_size")

    if len(text) <= max_chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = min(start + max_chunk_size, len(text))
        if end < len(text):
            sentence_break = text.rfind(".", start, end)
            if sentence_break != -1 and sentence_break > start + (max_chunk_size // 2):
                end = sentence_break + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        next_start = end - overlap
        if next_start <= start:
            next_start = end
        start = next_start

    return chunks


def chunk_by_sentences(text: str, sentences_per_chunk: int = 5) -> list[str]:
    if sentences_per_chunk <= 0:
        raise ValueError("sentences_per_chunk must be > 0")

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    sentences = [sentence for sentence in sentences if sentence.strip()]
    if not sentences:
        return []

    chunks: list[str] = []
    for index in range(0, len(sentences), sentences_per_chunk):
        chunk = " ".join(sentences[index : index + sentences_per_chunk]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks


def chunk_by_paragraphs(text: str, max_paragraphs: int = 3) -> list[str]:
    if max_paragraphs <= 0:
        raise ValueError("max_paragraphs must be > 0")

    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
    if not paragraphs:
        return []

    chunks: list[str] = []
    for index in range(0, len(paragraphs), max_paragraphs):
        chunk = "\n\n".join(paragraphs[index : index + max_paragraphs]).strip()
        if chunk:
            chunks.append(chunk)
    return chunks
