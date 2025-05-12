# 📰 News-RAG-Chatbot

A full-stack Retrieval-Augmented Generation (RAG) chatbot over a news corpus.  
Built with FastAPI (Python), React + Tailwind CSS, Chroma vector store, Redis session caching, and a mocked Google Gemini LLM for demo.

---

## 📁 Project Structure

project-root/

├── backend/ # FastAPI + RAG pipeline
│ ├── articles.json # Ingested news articles
│ ├── fetch_articles.py # Fetches raw articles from NewsAPI
│ ├── embed_articles.py # (Re-)embeds & stores articles in Chroma
│ ├── ingest.py # Loads articles.json into Chroma
│ ├── main.py # FastAPI app with /chat, /history, /reset_session
│ ├── requirements.txt # Python dependencies
│ └── .env # ENV vars (REDIS_URL, GEMINI_API_KEY)

├── frontend/ # React + Tailwind chatbot UI
│ ├── public/
│ ├── src/
│ │ ├── App.js
│ │ └── ChatScreen.js
│ ├── package.json
│ └── tailwind.config.js

├── chroma_db/ # On-disk Chroma store
├── chroma_store/ # (optional backup)
├── articles/ # Raw .txt article excerpts
├── .gitignore
└── README.md # ← you are here


---

## 🚀 Features

- **RAG Pipeline**  
  - Ingested ~50 news articles via NewsAPI  
  - Sentence-Transformer embeddings (all-MiniLM-L6-v2)  
  - Stored & retrieved from Chroma vector store  
- **Chat API**  
  - FastAPI endpoints:  
    - `POST /chat` for Q&A  
    - `GET /history/{session_id}`  
    - `DELETE /history/{session_id}`  
    - `POST /reset_session`  
  - Context retrieval → (mocked) Gemini call → reply  
- **Session Caching**  
  - Redis in-memory store with 1-hour TTL  
- **Frontend**  
  - React + Tailwind UI  
  - Chat screen, input box, “Fetching response…” placeholder, reset button  
- **Mock LLM**  
  - Dummy Gemini response; replace with real API when available  

---

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, FastAPI  
- **Embeddings:** `sentence-transformers`  
- **Vector DB:** Chroma (duckdb+parquet)  
- **Cache:** Redis  
- **Frontend:** React, Tailwind CSS  
- **LLM:** Google Gemini API (mocked)  

---

## 📥 Prerequisites

- Python 3.9+  
- Node.js 14+ & npm  
- Redis server running locally  
- (Optional) Google Gemini API key & billing enabled  

---

## 🔧 Setup and Run

cd backend
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # set REDIS_URL, GEMINI_API_KEY
# (Re)ingest articles:
python fetch_articles.py
python ingest.py
# Start API server:
uvicorn main:app --reload

cd ../frontend
npm install
npm start

Visit http://localhost:3000

Chat → backend logs at http://localhost:8000/docs
