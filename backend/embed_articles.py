import json
import os
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

# Set a persistent directory
PERSIST_DIR = os.path.join(os.getcwd(), "chroma_store")

# Create a persistent Chroma client
client = PersistentClient(path=PERSIST_DIR)

# Create or get collection
if "news_articles" in [col.name for col in client.list_collections()]:
    collection = client.get_collection("news_articles")
else:
    collection = client.create_collection(name="news_articles")

# Load articles
with open("articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed and upsert documents
for idx, article in enumerate(articles):
    text = f"{article['title']}\n{article['description']}"
    embedding = model.encode(text).tolist()
    collection.add(
        ids=[str(idx)],
        documents=[text],
        embeddings=[embedding],
        metadatas=[article]
    )

print("✅ Successfully embedded and stored all articles in Chroma.")
