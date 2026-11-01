from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app

client = TestClient(app)


def test_ask_devuelve_respuesta_y_fuentes():
    fake_passages = [("texto de prueba", {"source": "a.pdf", "page": 1})]
    with patch("app.main.search", return_value=fake_passages), \
         patch("app.main.answer", return_value="respuesta falsa"):
        r = client.post("/ask", json={"text": "hola"})

    assert r.status_code == 200
    assert r.json()["answer"] == "respuesta falsa"
    assert r.json()["sources"] == [{"source": "a.pdf", "page": 1}]


def test_ask_sin_texto_da_422():
    r = client.post("/ask", json={})
    assert r.status_code == 422