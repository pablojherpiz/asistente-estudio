import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from app.store import add_document, search
from app.llm import answer

app = FastAPI(title="Asistente de estudio")
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class Question(BaseModel):
    text: str


@app.post("/documents")
def upload(file: UploadFile):
    dest = UPLOAD_DIR / file.filename
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    add_document(dest)
    return {"status": "indexado", "file": file.filename}


@app.post("/ask")
def ask(q: Question):
    passages = search(q.text)
    return {
        "answer": answer(q.text, passages),
        "sources": [m for _, m in passages],
    }