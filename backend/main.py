import os
import uuid
import json
import redis
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # 👈 Added for CORS
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, MatchValue
from sentence_transformers import SentenceTransformer
import chromadb

# --- Config ---
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "DUMMY_KEY")

# --- Initialize services ---
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
app = FastAPI()

# 👇 Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] if you're strict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load embedding model
_model = SentenceTransformer('all-MiniLM-L6-v2')

# --- Chroma client ---
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="news_articles")

# --- Pydantic models ---
class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    answer: str
    session_id: str

# --- Helper: call dummy Gemini ---
def call_gemini(context: str, question: str) -> str:
    try:
        # Simulated dummy Gemini response
        return f"🤖 Dummy Gemini answer to: '{question}' with context: '{context[:100]}...'"
    except Exception as e:
        print("Gemini API call failed:", e)
        return "Sorry, I couldn't get a response from Gemini."

# --- Helper: Retrieve top-k context ---
def retrieve_context(question: str, k: int = 3) -> str:
    q_vec = _model.encode(question).tolist()
    results = collection.query(query_embeddings=[q_vec], n_results=k)
    contexts = []
    for meta in results["metadatas"][0]:
        title = meta.get("title", "")
        desc = meta.get("description", "")
        contexts.append(f"{title}: {desc}")
    return "\n\n".join(contexts)

# --- Endpoints ---

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    sess = req.session_id or str(uuid.uuid4())
    context = retrieve_context(req.message)
    answer = call_gemini(context, req.message)
    r.rpush(f"chat:{sess}", json.dumps({"user": req.message, "bot": answer}))
    r.expire(f"chat:{sess}", 3600)
    return {"answer": answer, "session_id": sess}

@app.get("/history/{session_id}")
def get_history(session_id: str):
    items = r.lrange(f"chat:{session_id}", 0, -1)
    return [json.loads(item) for item in items]

@app.delete("/history/{session_id}")
def clear_history(session_id: str):
    r.delete(f"chat:{session_id}")
    return {"status": "cleared"}

@app.post("/reset_session")
async def reset_session(session_id: str):
    try:
        r.delete(session_id)
        return JSONResponse(content={"message": "Session reset successful!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting session: {str(e)}")
