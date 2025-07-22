**Project Overview: News RAG Chatbot (Prototype)**

This is a **prototype of a Retrieval-Augmented Generation (RAG) based News Chatbot** designed to simulate how a real-world AI news assistant would work. The project demonstrates my ability to integrate a **React frontend** with a **FastAPI backend**, manage **stateful chat sessions**, and structure API endpoints for AI-based interactions.

Currently, this project uses **mock responses instead of live AI APIs (like Gemini, OpenAI)** to avoid unnecessary costs during development. The mock responses serve as placeholders to demonstrate the flow and behavior of the app.

### 🔍 **What This Project Demonstrates**

* Frontend and backend integration
* RESTful API creation with FastAPI
* Session-based conversation management
* Handling user input/output in a chat interface
* Preparing infrastructure ready for live AI API integration (Gemini, OpenAI, etc.)

## **How It Works (Currently)**

* The backend responds with **dummy AI-like responses** for any user input.
* The frontend is fully wired to interact with these backend endpoints.
* The mechanism simulates real-time AI chat behavior for the purpose of this prototype.

## **Tech Stack**

### **Frontend:**

* React.js (Vite)
* Tailwind CSS
* Axios (for API communication)

### **Backend:**

* Python
* FastAPI
* Redis (for session state management)
* ChromaDB (for prototype vector store simulation)
* Uvicorn (ASGI server)
* Sentence Transformers (planned for embedding, mocked for now)

##**Why Mock Responses?**

This project avoids using real AI APIs to:

* Keep costs at zero during development.
* Focus on demonstrating technical architecture, not API billing.
* Showcase frontend-backend integration readiness for future API connection.
