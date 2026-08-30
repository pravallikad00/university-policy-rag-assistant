from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()[
        "message"] == "University Policy RAG Assistant is running."


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_question_returns_source_document():
    response = client.post(
        "/ask",
        json={"question": "What are the graduation requirements?"}
    )

    data = response.json()

    assert response.status_code == 200
    assert "120 credit hours" in data["answer"]
    assert data["sources"][0]["document"] == "sample_policy.md"


def test_upload_rejects_non_pdf_file():
    response = client.post(
        "/upload-pdf",
        files={
            "file": (
                "notes.txt",
                b"This is not a PDF file.",
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Only PDF files are allowed."
