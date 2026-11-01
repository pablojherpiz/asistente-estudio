from pypdf import PdfReader


def load_pdf(path):
    """Devuelve (numero_de_pagina, texto) por cada página."""
    reader = PdfReader(path)
    for page_num, page in enumerate(reader.pages, start=1):
        yield page_num, page.extract_text() or ""


def chunk_text(text, size=800, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        piece = text[start:start + size].strip()
        if piece:
            chunks.append(piece)
        start += size - overlap
    return chunks