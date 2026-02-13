"""Quick test: Google Custom Search API credentials."""
import urllib.request
import urllib.parse
import json
import sys

API_KEY = "AIzaSyAJz4oti9lmZOZQdDs7UCB0gAUixjvie_k"
CX = "76af6bd1a60b54f6d"
QUERY = "hello world"

url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={urllib.parse.quote(QUERY)}&num=2"

try:
    r = urllib.request.urlopen(url, timeout=10)
    data = json.loads(r.read())
    items = data.get("items", [])
    print(f"STATUS: OK ({len(items)} results)")
    for i in items:
        print(f"  - {i['title']}")
        print(f"    {i['link']}")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"STATUS: HTTP ERROR {e.code}")
    print(f"  {body[:500]}")
except Exception as e:
    print(f"STATUS: ERROR - {e}")
