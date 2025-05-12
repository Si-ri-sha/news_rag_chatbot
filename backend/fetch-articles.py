import os
import json
import requests

API_KEY = "64aa197b0a264005841387be4f144057"  # replace with your NewsAPI key
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# Create the articles directory if it doesn't exist
os.makedirs("articles", exist_ok=True)

article_count = 0
page = 1
all_articles = []  # List to collect all articles

while article_count < 50:
    params = {
        'apiKey': API_KEY,
        'country': 'us',
        'pageSize': 50,
        'page': page
    }

    response = requests.get(NEWS_API_URL, params=params)
    
    if response.status_code != 200:
        print(f"Not a 200 response: {response.status_code}")
        break

    articles = response.json().get('articles', [])

    if not articles:
        print("No more articles found.")
        break

    for article in articles:
        if article_count >= 50:
            break

        title = article.get('title')
        description = article.get('description')
        url = article.get('url')

        if title and description:
            # Save individual text file
            with open(f"articles/article_{article_count + 1}.txt", "w", encoding="utf-8") as f:
                f.write(f"Title: {title}\n")
                f.write(f"Description: {description}\n")
                f.write(f"URL: {url}\n")
            
            # Save to JSON list
            all_articles.append({
                "title": title,
                "description": description,
                "url": url
            })

            print(f"Saved article {article_count + 1}")
            article_count += 1

    page += 1

# Save all articles into a single JSON file
with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, indent=2)

print("✅ All articles saved to individual .txt files and articles.json")
