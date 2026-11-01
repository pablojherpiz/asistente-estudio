import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.store import add_document, search, clear_documents
from app.llm import answer

app = FastAPI(title="Asistente de estudio")
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
INDEX = Path(__file__).parent / "static" / "index.html"


class Question(BaseModel):
    text: str


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(INDEX)


@app.post("/documents")
def upload(file: UploadFile):
    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    add_document(dest)
    return {"status": "indexado", "file": file.filename}


@app.delete("/documents")
def clear():
    clear_documents()
    for f in UPLOAD_DIR.glob("*"):
        f.unlink()
    return {"status": "borrado"}


@app.post("/ask")
def ask(q: Question):
    passages = search(q.text)
    return {
        "answer": answer(q.text, passages),
        "sources": [m for _, m in passages],
    }