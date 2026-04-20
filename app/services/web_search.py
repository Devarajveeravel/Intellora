import requests

def search_web(query: str):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        res = requests.get(url).json()

        results = []

        # Get only meaningful text
        if "RelatedTopics" in res:
            for item in res["RelatedTopics"][:3]:
                if "Text" in item:
                    results.append(item["Text"])

        return "\n".join(results)

    except:
        return ""