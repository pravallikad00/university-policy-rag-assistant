# University Policy RAG Assistant

A beginner-friendly Retrieval-Augmented Generation (RAG) project that answers university policy and course-related questions from source documents.

## Current Features

- FastAPI backend with interactive Swagger API documentation
- Health-check endpoint for application status
- Question-answering endpoint: `POST /ask`
- Document-based keyword retrieval from a university-policy source file
- Source citation showing the document and matching policy section

## Project Structure

```text
app/
  main.py                 # FastAPI application and retrieval logic
data/
  sample_policy.md        # Sample university policy source document
requirements.txt          # Python dependencies
