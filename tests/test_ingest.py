from app.ingest import chunk_text


def test_chunks_no_superan_el_tamano():
    text = "a" * 2000
    chunks = chunk_text(text, size=800, overlap=100)
    assert all(len(c) <= 800 for c in chunks)


def test_texto_vacio_no_genera_chunks():
    assert chunk_text("") == []


def test_hay_solapamiento():
    text = "abcdefghij" * 100
    chunks = chunk_text(text, size=100, overlap=20)
    assert chunks[0][-20:] == chunks[1][:20]