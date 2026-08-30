from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(
    title="University Policy RAG Assistant",
    description="An API that answers university policy and course questions using local document retrieval.",
    version="0.4.0",
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
POLICY_FILE = DATA_DIR / "sample_policy.md"
UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


class QuestionRequest(BaseModel):
    question: str


def split_into_chunks(text: str, chunk_size: int = 900) -> list[str]:
    clean_text = " ".join(text.split())

    return [
        clean_text[index:index + chunk_size]
        for index in range(0, len(clean_text), chunk_size)
    ]


def get_document_chunks() -> list[dict]:
    document_paths = [POLICY_FILE, *UPLOAD_DIR.glob("*.txt")]
    chunks = []

    for document_path in document_paths:
        if not document_path.exists():
            continue

        text = document_path.read_text(encoding="utf-8")

        for chunk in split_into_chunks(text):
            chunks.append(
                {
                    "document": document_path.name,
                    "content": chunk
                }
            )

    return chunks


def find_relevant_section(question: str) -> dict:
    document_chunks = get_document_chunks()

    if not document_chunks:
        return {
            "answer": "No documents are available for searching.",
            "sources": []
        }

    chunk_texts = [chunk["content"] for chunk in document_chunks]

    vectorizer = TfidfVectorizer(stop_words="english")
    document_vectors = vectorizer.fit_transform(chunk_texts)
    question_vector = vectorizer.transform([question])

    similarity_scores = cosine_similarity(
        question_vector,
        document_vectors
    ).flatten()

    best_index = similarity_scores.argmax()
    best_score = float(similarity_scores[best_index])
    best_chunk = document_chunks[best_index]

    if best_score == 0:
        return {
            "answer": "I could not find a matching answer in the available documents.",
            "sources": []
        }

    return {
        "answer": best_chunk["content"],
        "sources": [
            {
                "document": best_chunk["document"],
                "relevance_score": round(best_score, 3)
            }
        ]
    }


@app.get("/")
def home():
    return {"message": "University Policy RAG Assistant is running."}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    filename = Path(file.filename or "uploaded_document.pdf").name

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    pdf_path = UPLOAD_DIR / filename
    pdf_path.write_bytes(await file.read())

    reader = PdfReader(pdf_path)
    extracted_text = "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    ).strip()

    if not extracted_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text was found in this PDF."
        )

    text_path = UPLOAD_DIR / f"{pdf_path.stem}.txt"
    text_path.write_text(extracted_text, encoding="utf-8")

    return {
        "message": "PDF uploaded and processed successfully.",
        "pdf_file": pdf_path.name,
        "text_file": text_path.name,
        "characters_extracted": len(extracted_text)
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = find_relevant_section(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }


app.mount("/app", StaticFiles(directory="static", html=True), name="web_app")
