# Airror

Airror is a Python debugging assistant that helps map runtime errors to relevant code and generate fix suggestions using an LLM.

## What it does

- Parses Python repositories and extracts function-level code blocks.
- Builds a searchable Whoosh index over parsed code.
- Searches indexed code using BM25-based multi-field retrieval.
- Parses traceback text to extract error type and message.
- Sends error + retrieved snippets to Gemini or Groq for explanation and suggested fixes.
- Exposes both CLI and FastAPI interfaces.

## Project structure

- `/parser`
  - `code_parser.py`: AST-based Python function extraction.
  - `error_parser.py`: traceback parsing into structured error data.
- `/index`
  - `schema.py`: Whoosh schema definition.
  - `build_index.py`: index creation/loading in `data/index`.
- `/search`
  - `bm25_search.py`: BM25 retrieval over indexed code fields.
  - `pageindex_search.py`: utility for fetching indexed docs.
  - `context_retrieval.py`: surrounding-code helper (currently sample-repo focused).
- `/llm`
  - `prompts.py`: prompt templates.
  - `explain.py`: provider-specific LLM calls (Gemini, Groq).
- `/api`
  - `main.py`: FastAPI app with `/index` and `/query`.
  - `schemas.py`: request schema models.
- `cli.py`: Typer CLI entrypoint.
- `/repos/sample_repo`: intentionally buggy sample Python code.

## Installation

```bash
python -m pip install -r requirements.txt
```

Optional editable install:

```bash
python -m pip install -e .
```

## Environment variables

Set at least one provider key depending on usage:

- `GEMINI_API_KEY` for Gemini provider (default)
- `GROQ_API_KEY` for Groq provider

## CLI usage

Build index from a repository:

```bash
python /tmp/workspace/rishabhpandey106/airror/cli.py index /absolute/path/to/repo
```

Query with a traceback:

```bash
python /tmp/workspace/rishabhpandey106/airror/cli.py query "ZeroDivisionError: division by zero" --provider gemini --project-path /absolute/path/to/repo
```

## API usage

Start server:

```bash
uvicorn api.main:app --reload
```

Index repository:

```bash
curl -X POST "http://127.0.0.1:8000/index?path=/absolute/path/to/repo"
```

Query error:

```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "error": "ZeroDivisionError: division by zero",
    "provider": "gemini",
    "project_path": "/absolute/path/to/repo"
  }'
```

## Running tests

```bash
PYTHONPATH=. pytest -q
```

Note: some current test files behave like executable scripts rather than strict unit tests, and parts of the test run may require local environment setup (for example API keys).

## Current limitations

- Python-focused parsing (`.py` files only).
- Index directory is fixed to `data/index` in index builder/search loader.
- `context_retrieval.py` currently uses a sample hardcoded repository path.
- LLM output parsing may return fallback plain text when JSON decoding fails.
