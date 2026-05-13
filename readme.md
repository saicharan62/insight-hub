# InsightHub

> **Turn raw notes into structured knowledge — automatically.**

InsightHub is a lightweight, full-stack AI system that processes your notes and surfaces what actually matters: key points, action items, open questions, tone, and tags. It also clusters semantically related insights so you can discover connections across your own thinking over time.

---

## Table of Contents

- [The Problem](#the-problem)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Example Response](#example-response)
- [Roadmap](#roadmap)
- [License](#license)

---

## The Problem

Notes accumulate faster than they can be reviewed. A meeting note, a news article, a half-formed idea — they pile up as unstructured text with no summary, no tags, no way to see which thoughts are related. Extracting value from a personal knowledge base is a manual chore.

InsightHub automates that extraction. Write a note, hit save, and the system immediately produces a summary, sentiment, keywords, and a structured insight breakdown. Over time, similar notes get clustered together, revealing patterns and connections you wouldn't have spotted manually.

---

## Features

**Authentication**
- JWT-based registration and login
- All insight endpoints are protected

**Insight Engine**
- Create, read, update, and delete personal insights
- Automatic NLP processing on every save: summary, keyword extraction, and sentiment analysis via HuggingFace Transformers and KeyBERT
- AI-driven structured extraction returning key points, action items, open questions, tone, and tags

**Semantic Clustering**
- Each insight is embedded using SentenceTransformer (`all-MiniLM-L6-v2`)
- Insights are incrementally grouped by similarity into clusters
- A dedicated Cluster View surfaces related thoughts side by side

**Frontend**
- Single-page React + Tailwind interface
- Create and browse insights
- Trigger structured extraction on any note
- View semantic clusters
- Minimal, clean aesthetic

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| NLP | HuggingFace Transformers, KeyBERT |
| Embeddings | SentenceTransformer (`all-MiniLM-L6-v2`) |
| Database | PostgreSQL |
| Auth | JWT |
| Frontend | React, Vite, TailwindCSS |
| Infra | Docker-ready |

---

## Repository Structure

```
insight-hub/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── db.py                # Database session and connection
│   │   ├── core/
│   │   │   ├── nlp.py           # Summary, sentiment, keyword extraction
│   │   │   ├── embeddings.py    # SentenceTransformer embedding logic
│   │   │   └── auth.py          # JWT utilities
│   │   ├── routes/
│   │   │   ├── insights.py      # CRUD endpoints
│   │   │   ├── extract.py       # Structured AI extraction endpoint
│   │   │   └── auth.py          # Register / login endpoints
│   │   ├── models/              # SQLAlchemy models (User, Insight, InsightEmbedding)
│   │   └── schemas/             # Pydantic request/response schemas
├── insighthub-ui/
│   ├── src/
│   │   ├── InsightHubApp.tsx    # Root application component
│   │   └── ...
│   └── index.html
├── requirements.txt
└── README.md
```

---

## Prerequisites

- Python ≥ 3.10
- Node.js ≥ 18
- PostgreSQL (running and accessible)
- (Optional) Docker, for containerised deployment

---

## Setup

### Backend

**1. Install Python dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**2. Configure environment variables**

Create a `.env` file in the `backend/` directory (see [Environment Variables](#environment-variables) below).

**3. Run database migrations**

```bash
alembic upgrade head
```

**4. Start the API server**

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

---

### Frontend

**1. Install dependencies**

```bash
cd insighthub-ui
npm install
```

**2. Start the development server**

```bash
npm run dev
```

The UI will be available at `http://localhost:5173`.

If the backend is running on a different host or port, set the API base URL before the app loads:

```javascript
window.__INSIGHTHUB_API_BASE__ = "http://<host>:8000";
```

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost/insighthub` |
| `JWT_SECRET` | Secret key for signing JWT tokens | `a-long-random-string` |

---

## API Reference

### Auth

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/register` | Create a new user account |
| `POST` | `/auth/login` | Authenticate and receive a JWT |

### Insights

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/insights/` | Create a new insight (triggers NLP processing) |
| `GET` | `/insights/` | List all insights for the authenticated user |
| `PATCH` | `/insights/{id}` | Update an existing insight |
| `DELETE` | `/insights/{id}` | Delete an insight |

### Extraction & Clustering

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/insights/{id}/extract` | Run structured AI extraction on a single insight |
| `GET` | `/insights/clusters` | Return all insights grouped by semantic similarity |

All endpoints except `/auth/register` and `/auth/login` require an `Authorization: Bearer <token>` header.

---

## Example Response

`GET /insights/{id}/extract`

```json
{
  "key_points": [
    "Pakistan initiated drone retaliation across the eastern border"
  ],
  "action_items": [],
  "tone": "neutral / observational",
  "questions": [],
  "tags": ["drone", "defence", "geopolitics"]
}
```

---

## Roadmap

- [ ] Full CRUD actions in the UI (edit and delete)
- [ ] Global search and tag-based filtering
- [ ] VectorDB backend (Qdrant / Weaviate) for scalable similarity search
- [ ] Conversational AI interface trained on the user's own insights

---

## License

MIT © [saicharan62](https://github.com/saicharan62)
