import requests
from requests import get

#Semantic Scholar 
SS_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def find_most_relevant_paper(query):
    print("Search Semantic Scholar for the most relevant paper on a topic.")
    url = f"{SS_BASE_URL}"
    params = {
        "query": query,
        "fields": "title,url,year,citationCount,paperId",
        "limit": 1  # Get the top result
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    
    if "data" in data and len(data["data"]) > 0:
        top_paper = data["data"][0]
        return {
            "title": top_paper.get("title", "Unknown"),
            "url": top_paper.get("url", ""),
            "year": top_paper.get("year", "N/A")
        }
    
    return None

def find_influential_citations(url):
    print("Search Most Influential Citations")


topic = "Gaussian Splatting"
most_relevant_paper = find_most_relevant_paper(topic)
print(most_relevant_paper)

?citedSort=is-influential