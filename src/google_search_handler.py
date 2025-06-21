import os
from googleapiclient.discovery import build

def google_search(query, api_key, cse_id, num=5):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num).execute()
    results = []
    for item in res.get('items', []):
        results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet")
        })
    return results
