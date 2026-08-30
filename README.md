# University Policy RAG Assistant

A local document-retrieval application that helps users upload approved university policy PDFs and ask questions using source-based retrieval.

## Features

- Upload PDF policy and course-information documents
- Extract text from PDFs using `pypdf`
- Store uploaded files locally without committing them to GitHub
- Split documents into searchable text chunks
- Rank relevant content using TF-IDF retrieval with scikit-learn
- Return document-based answers with source citations
- Interactive FastAPI API documentation
- Simple browser interface for PDF upload and questions
- Automated API tests with pytest
- GitHub Actions workflow that runs tests on every push

## Technology Stack

- Python
- FastAPI
- pypdf
- scikit-learn
- HTML, CSS, JavaScript
- pytest
- GitHub Actions

## Project Structure

```text
app/
  main.py                  # API, PDF processing, and retrieval logic
data/
  sample_policy.md         # Sample source document
  uploads/                 # Local PDF uploads; excluded from Git
static/
  index.html               # Browser interface
tests/
  test_api.py              # Automated API tests
.github/workflows/
  tests.yml                # GitHub Actions test workflow