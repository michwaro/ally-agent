"""FastAPI app for streaming Ally orchestrator events."""

from __future__ import annotations

import io
import json
from collections.abc import Iterator
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from pypdf import PdfReader

from ally.orchestrator import Event, orchestrate

ROOT = Path(__file__).resolve().parents[2]
WEB_DIR = ROOT / "web"
INDEX_PATH = WEB_DIR / "index.html"
ALLOWED_ORIGINS = ["http://localhost:8765", "http://127.0.0.1:8765"]

app = FastAPI(title="Ally")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    report_text: str


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(INDEX_PATH)


@app.get("/web/{filename:path}")
def web_file(filename: str) -> FileResponse:
    file_path = (WEB_DIR / filename).resolve()
    web_root = WEB_DIR.resolve()
    if web_root not in file_path.parents and file_path != web_root:
        raise HTTPException(status_code=400, detail="Invalid web path")
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


def _sse_event(name: str, data: dict[str, object]) -> str:
    return f"event: {name}\ndata: {json.dumps(data)}\n\n"


def _stream_report(report_text: str) -> Iterator[str]:
    for event in orchestrate(report_text):
        yield _sse_event("progress", event.to_dict())
        if _is_pipeline_done(event):
            report = event.evidence[0] if event.evidence else ""
            yield _sse_event("done", {"report": report})
            return


def _is_pipeline_done(event: Event) -> bool:
    return event.agent == "Pipeline" and event.status == "completed"


@app.post("/api/run-stream")
def run_stream(payload: RunRequest) -> StreamingResponse:
    return StreamingResponse(_stream_report(payload.report_text), media_type="text/event-stream")


@app.post("/api/upload-report")
async def upload_report(file: UploadFile = File(...)) -> dict[str, str]:
    filename = file.filename or ""
    suffix = Path(filename).suffix.lower()
    contents = await file.read()
    if suffix == ".txt":
        report_text = contents.decode("utf-8")
    elif suffix == ".pdf":
        report_text = _extract_pdf_text(contents)
    else:
        raise HTTPException(status_code=400, detail="Only .txt and .pdf files are supported")
    return {"report_text": report_text.strip()}


def _extract_pdf_text(contents: bytes) -> str:
    reader = PdfReader(io.BytesIO(contents))
    return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
