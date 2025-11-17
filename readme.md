InsightHub - A Minimal AI-Powered Personal Knowledge Engine

🚀 Overview

InsightHub is a lightweight, full-stack AI system that transforms user notes into structured insights.

It performs:
Automatic NLP processing – summary, sentiment, keywords
Vector embedding \& clustering of insights
AI-assisted insight extraction (key points, action items, questions, tone)
Clean frontend built with React + Tailwind
Secure API using FastAPI + PostgreSQL + JWT Auth
The system is designed to serve as a personal knowledge base, research assistant, and insight generator, all in one minimal interface.

🧠 Core Features
🔐 Authentication
JWT-based secure login \& registration
Protected Insight endpoints

📝 Insight Engine
Create, update, delete personal insights
Automatic summary, keyword extraction \& sentiment via transformers
AI-driven “Insight Extraction” with:
Key points
Action items
Questions
Tone
Tags

🧬 Semantic Clustering
SentenceTransformer embeddings
Incremental similarity-based cluster formation
“Cluster View” to see related thoughts grouped together

💡 Frontend (React + Tailwind)
Single-page interface
Create \& view insights
Extract insights from any note
View semantic clusters
Minimal clean UI (Apple-style aesthetic)



🏗️ Tech Stack

Layer	Technology

Backend	FastAPI, SQLAlchemy, Pydantic

NLP	HuggingFace Transformers, KeyBERT

Embeddings	SentenceTransformer (MiniLM-L6-v2)

DB	PostgreSQL

Auth	JWT

Frontend	React + Vite + TailwindCSS

Infra	Docker-ready

📂 Repository Structure

insight-hub/

│

├── backend/

│   ├── app/

│   │   ├── main.py

│   │   ├── core/ (NLP, embedding, auth)

│   │   ├── routes/ (insights, auth, extract)

│   │   ├── models/ (Insight, InsightEmbedding, User)

│   │   ├── schemas/

│   │   └── db.py

│

├── insighthub-ui/

│   ├── src/

│   │   ├── InsightHubApp.tsx

│   │   └── ...

│   └── index.html

│

└── README.md



⚙️ Setup Instructions

1️⃣ Backend Setup

cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload





You must set environment variables:



DATABASE\_URL=postgresql://user:pass@localhost/insighthub

JWT\_SECRET=your\_secret



2️⃣ DB Migration

alembic upgrade head



3️⃣ Frontend Setup

cd insighthub-ui

npm install

npm run dev





If backend runs on another host/port, set:



window.\_\_INSIGHTHUB\_API\_BASE\_\_ = "http://<host>:8000"



🔑 API Highlights

Endpoint	Method	Description

/auth/register	POST	Create user

/auth/login	POST	Get JWT

/insights/	POST	Create insight

/insights/	GET	Get all insights

/insights/{id}	PATCH	Update insight

/insights/{id}	DELETE	Delete insight

/insights/{id}/extract	GET	Extract structured insight

/insights/clusters	GET	Get semantic clusters

🧪 Example Extract Response

{

&nbsp; "key\_points": \["Pakistan initiated drone retaliation..."],

&nbsp; "action\_items": \[],

&nbsp; "tone": "neutral / observational",

&nbsp; "questions": \[],

&nbsp; "tags": \["drone","defence","iccs"]

}



🏁 Roadmap



🔄 Full CRUD in UI (update + delete)



🔍 Global search \& filters



🧭 VectorDB support



🧑‍💻 AI chatbot trained on user’s insights



📜 License



MIT (Open use allowed)

