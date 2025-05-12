import json
import chromadb
from sentence_transformers import SentenceTransformer

# Load model and Chroma client
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="news_articles")

# Load articles
with open("articles.json", "r") as f:
    articles = json.load(f)

# Prepare data
documents = [f"{a['title']} - {a['description']}" for a in articles]
metadatas = [{"title": a["title"], "description": a["description"], "url": a["url"]} for a in articles]
ids = [f"doc-{i}" for i in range(len(articles))]

# Embed and add to Chroma
embeddings = model.encode(documents).tolist()
collection.add(documents=documents, embeddings=embeddings, metadatas=metadatas, ids=ids)

print(f"✅ Ingested {len(documents)} articles.")
