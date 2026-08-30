from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="University Policy RAG Assistant",
    description="An API that answers university policy and course questions using source documents.",
    version="0.2.0",
)

POLICY_FILE = Path(__file__).resolve().parent.parent / \
    "data" / "sample_policy.md"


class QuestionRequest(BaseModel):
    question: str


def find_relevant_section(question: str) -> dict:
    policy_text = POLICY_FILE.read_text(encoding="utf-8")

    sections = [
        section.strip()
        for section in policy_text.split("## ")
        if section.strip()
    ]

    question_words = {
        word.lower().strip(".,?!")
        for word in question.split()
        if len(word) > 2
    }

    best_section = ""
    best_score = 0

    for section in sections:
        section_words = set(section.lower().split())
        score = len(question_words.intersection(section_words))

        if score > best_score:
            best_score = score
            best_section = section

    if best_score == 0:
        return {
            "answer": "I could not find a matching answer in the available policy document.",
            "sources": []
        }

    title, content = best_section.split("\n", 1)

    return {
        "answer": content.replace("\n", " "),
        "sources": [
            {
                "document": "sample_policy.md",
                "section": title,
                "relevance_score": best_score
            }
        ]
    }


@app.get("/")
def home():
    return {"message": "University Policy RAG Assistant is running."}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = find_relevant_section(request.question)

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }
