import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.ingest import load_pdf, load_web, split_documents
from backend.vector_store import save_vectors
from backend.rag_pipeline import get_qa_chain
from backend.source_manager import (
    load_sources,
    add_source,
    delete_source
)
from backend.config import PDF_STORAGE_PATH


app = FastAPI(title="RAGnosis")

app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/")
def serve_ui():
    return FileResponse("frontend/index.html")


# ------------------ Models ------------------

class Query(BaseModel):
    question: str


class URLRequest(BaseModel):
    url: str


# ------------------ Ingestion ------------------

@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    os.makedirs(PDF_STORAGE_PATH, exist_ok=True)
    pdf_path = f"{PDF_STORAGE_PATH}/{file.filename}"

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    docs = load_pdf(pdf_path)
    chunks = split_documents(docs)
    save_vectors(chunks)

    add_source("pdf", pdf_path)

    return {"message": "PDF ingested successfully"}


@app.post("/ingest/url")
def ingest_url(req: URLRequest):
    docs = load_web(req.url)
    chunks = split_documents(docs)
    save_vectors(chunks)

    add_source("url", req.url)

    return {"message": "URL ingested successfully"}


# ------------------ Sources ------------------

@app.get("/sources")
def get_sources():
    return load_sources()


@app.delete("/sources")
def remove_source(value: str):
    delete_source(value)
    return {"message": "Source deleted"}


# ------------------ Chat ------------------

@app.post("/ask")
def ask(query: Query):
    try:
        chain = get_qa_chain()
        answer = chain.invoke(query.question)
        return {"answer": answer}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
