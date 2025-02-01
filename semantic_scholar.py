import requests
from requests import get
import time

from datatypes import Node

#Semantic Scholar 
SS_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def find_most_relevant_paper(query) -> Node:
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
        return Node(
            name = top_paper.get("title", "Unknown"),
            url = top_paper.get("url", ""),
            paper_id = top_paper.get("paperId", None)
        )
    
    return None


def fetch_paper_details(paper_id, retries=5, delay=3) -> dict:
    api_url = f"https://api.semanticscholar.org/v1/paper/{paper_id}"
    
    for attempt in range(retries):
        response = requests.get(api_url)
        
        if response.status_code == 200:
            return response.json()  # Successfully retrieved data
        
        elif response.status_code == 202:
            print(f"Attempt {attempt+1}: Data is being processed. Retrying in {delay} seconds...")
            time.sleep(delay)  # Wait before retrying
        
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None  # Stop on unexpected errors
    
    print("Max retries reached. Could not fetch paper details.")
    return None

def get_influential_papers(paper_id) -> list[Node]:
    details = fetch_paper_details(paper_id)
    if details is None:
        raise Exception("Not found")
    influential_papers = []
    for reference in details.get("references", []):
        if reference.get("isInfluential", False):
            influential_papers.append(
                Node(
                    name = reference.get("title", "Unknown"),
                    url = reference.get("url", ""),
                    paper_id = reference.get("paperId", None)
                )
            )
    return influential_papers


topic = "Gaussian Splatting"
most_relevant_paper = find_most_relevant_paper(topic)
print(most_relevant_paper)
influential_papers = get_influential_papers(most_relevant_paper.paper_id)
print(influential_papers)

#https://www.semanticscholar.org/paper/3D-Gaussian-Splatting-for-Real-Time-Radiance-Field-Kerbl-Kopanas/2cc1d857e86d5152ba7fe6a8355c2a0150cc280a?citedSort=is-influential