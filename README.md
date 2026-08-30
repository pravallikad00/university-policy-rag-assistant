# University Policy RAG Assistant

A local document-retrieval application built to make university policy and course-information documents easier to search.

## Project Overview

University policy information is often stored in lengthy PDF documents such as academic catalogs, attendance policies, graduation requirements, and student-support guides. Finding the correct information manually can be slow and inconsistent.

This project provides a simple browser-based application where a user can upload an approved PDF document and ask a question. The application extracts the document text, splits it into searchable chunks, ranks the most relevant content, and returns the matching source text with a citation.

This is a local proof of concept built as a portfolio project. It is intended for use cases such as academic advising, student services, help-desk support, and policy-document search.

## Intended Users

- Students looking for policy or course information
- Academic advisors supporting student questions
- Student-services and help-desk teams
- University staff who need to search approved documents quickly

## Key Features

- Upload approved PDF policy and course-information documents
- Extract readable text from uploaded PDFs
- Store uploaded files locally
- Split extracted content into manageable text chunks
- Rank relevant content using TF-IDF retrieval
- Return source-based answers with document citations
- Provide a browser interface for uploading files and asking questions
- Expose REST APIs with interactive Swagger documentation
- Run automated API tests with pytest
- Run automated tests on every GitHub push using GitHub Actions

## How It Works

1. A user uploads an approved PDF through the browser interface.
2. The API validates that the uploaded file is a PDF.
3. `pypdf` extracts readable text from the document.
4. The application stores the extracted text locally.
5. The text is split into searchable chunks.
6. When a user asks a question, TF-IDF ranks the chunks by relevance.
7. The application returns the best matching content and identifies the source document.

## Technology Stack

| Technology | Usage in This Project |
|---|---|
| Python | Backend application development |
| FastAPI | REST APIs, file upload endpoint, question endpoint, health check, and Swagger documentation |
| pypdf | PDF text extraction |
| scikit-learn | TF-IDF vectorization and relevance ranking |
| HTML | Browser interface structure |
| CSS | Browser interface styling |
| JavaScript | Upload and question-answering interactions with the API |
| pytest | Automated API testing |
| httpx | Test-client support for API testing |
| Git | Version control |
| GitHub | Source-code hosting and portfolio repository |
| GitHub Actions | Continuous integration and automatic test execution |

## Project Structure

```text
university-policy-rag-assistant/
├── app/
│   ├── __init__.py
│   └── main.py                 # FastAPI application, PDF processing, and retrieval logic
├── data/
│   ├── sample_policy.md        # Sample university-policy source document
│   └── uploads/                # Local uploaded PDFs and extracted text; excluded from Git
├── static/
│   └── index.html              # Browser interface
├── tests/
│   └── test_api.py             # Automated API tests
├── .github/
│   └── workflows/
│       └── tests.yml           # GitHub Actions workflow
├── .gitignore
├── requirements.txt
└── README.md