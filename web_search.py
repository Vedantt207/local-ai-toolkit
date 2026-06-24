import requests
import json
import sys

def search_web(query, num_results=5):
    try:
        url = f"http://localhost:8080/search?q={query}&format=json&categories=general"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        results = []
        for r in data.get('results', [])[:num_results]:
            results.append({
                'title': r.get('title', ''),
                'url': r.get('url', ''),
                'content': r.get('content', '')[:500]
            })
        
        return json.dumps(results, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(search_web(query))
    else:
        print("Usage: python web_search.py <query>")