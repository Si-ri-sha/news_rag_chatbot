import requests
import json

GEMINI_API_KEY = "your_actual_gemini_api_key_here"  # Replace with your actual API key
context = "Example context for testing."
question = "What is the news?"

url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

payload = {
    "contents": [
        {
            "parts": [
                {"text": f"Use the following context to answer the question.\n\nContext:\n{context}\n\nQuestion: {question}"}
            ]
        }
    ]
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print("Response from Gemini API:", response.json())
else:
    print("Error with Gemini API request:", response.status_code, response.text)
