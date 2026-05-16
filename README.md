
# Query Intelligence Endpoint

This repository contains the backend used in the project: a small FastAPI service that accepts natural-language queries, calls an LLM (Anthropic with Groq fallback), stores the extracted structured response in a local SQLite database, and exposes two endpoints for create and fetch operations.

```text
backend/
├── app/
│   ├── main.py                 # FastAPI app entry and sync startup
│   ├── routes/queries.py       # POST /queries and GET /queries/{id}
│   ├── db/database.py          # synchronous SQLAlchemy engine & session
│   ├── models/query_model.py   # Query ORM with `llm_provider` and `extracted_data`
│   ├── services/llm_service.py # Anthropic primary, Groq fallback (sync)
│   └── schemas/query_schema.py # Pydantic request/response models
└── research.db                 # SQLite DB created at runtime (if present)
```

---

## Overview

This backend performs the following flow for each incoming query:

- Receive a JSON POST request to `POST /queries` with payload `{ "query": "..." }`.
- Call `app.services.llm_service.extract_structured_data()` to extract structured JSON from the prompt. Anthropic is used as the primary provider and Groq is used as a fallback.
- Persist a `Query` row with `raw_query`, `llm_provider`, and `extracted_data` (stored as JSON text) into the local SQLite file `research.db`.
- Return a JSON response that includes `id`, `query`, `llm_provider`, and `extracted_data`.
---

## Backend Setup

Ensure your virtual environment and dependencies are installed (see `requirements.txt`). To run the backend locally:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The server listens at `http://127.0.0.1:8000` and exposes swagger at `/docs`.

The database file used by the app is `research.db` in the repository root. If it does not exist, the app will create tables on startup.

---

## API Endpoints

### `POST /queries`

Request body: `{"query": "<natural language query>"}`

Behavior: calls the LLM extraction pipeline and stores the returned provider and extracted JSON in `Query.extracted_data`.

Response fields (example):
- `id`: integer DB id
- `query`: original query string
- `llm_provider`: string (e.g. `anthropic` or `groq (fallback)`)
- `extracted_data`: parsed JSON object returned by the LLM

### `GET /queries/{id}`

Returns stored `id`, `query`, `llm_provider`, and parsed `extracted_data` for a persisted query.

---

## API Example

Request:

```json
{
    "query":"What is fastest growing fintech startup in India?"
}
```

Stored / returned response (example):

```json
{
    "id": 1,
    "query": "What is fastest growing fintech startup in India?",
    "llm_provider": "groq (fallback)",
    "extracted_data": {
        "query": "What is fastest growing fintech startup in India?",
        "entities": {
            "location": "India",
            "industry": "fintech",
            "question_type": "fastest growing startup"
        },
        "answers": null,
        "related_queries": [
            "fastest growing fintech startups in India",
            "top fintech startups in India",
            "fintech industry in India"
        ],
        "entities_extracted": {
            "startup": null,
            "growth_rate": null
        }
    }
}
```

This shows `llm_provider` set to the fallback provider and `extracted_data` containing the LLM-parsed JSON structure.


---
# Author

**Varun Iyer**

Created as part of the **Spark Studios Internship Assignment**.
