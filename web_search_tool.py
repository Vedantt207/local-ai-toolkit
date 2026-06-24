from pydantic import BaseModel, Field
import requests
import json

class Tools:
    class Valves(BaseModel):
        searxng_url: str = Field(default="http://localhost:8080", description="SearXNG server URL")
    
    class UserValves(BaseModel):
        num_results: int = Field(default=5, description="Number of search results")
    
    def __init__(self):
        self.valves = self.Valves()
        self.user_valves = self.UserValves()
    
    async def web_search(self, query: str) -> str:
        \"\"\"Search the web for current information using SearXNG.\"\"\"
        try:
            url = f"{self.valves.searxng_url}/search?q={query}&format=json&categories=general"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            results = []
            for r in data.get('results', [])[:self.user_valves.num_results]:
                results.append(f"Title: {r.get('title', '')}")
                results.append(f"URL: {r.get('url', '')}")
                results.append(f"Content: {r.get('content', '')[:300]}")
                results.append("---")
            
            return "\n".join(results) if results else "No results found."
        except Exception as e:
            return f"Search error: {str(e)}"
