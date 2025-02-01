import requests

# Semantic Scholar API endpoint
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def find_most_relevant_paper(query, fields="title,url,year,citationCount"):
    """Search for the most relevant paper on a given topic using Semantic Scholar."""
    params = {
        "query": query,
        "fields": fields,
        "limit": 1,  # Get the top result
    }
    
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return f"Error: {response.status_code}, {response.text}"
    
    data = response.json()
    
    if "data" in data and len(data["data"]) > 0:
        top_paper = data["data"][0]
        return {
            "title": top_paper.get("title", "Unknown"),
            "url": top_paper.get("url", ""),
            "year": top_paper.get("year", "N/A"),
            "citationCount": top_paper.get("citationCount", 0),
            "paperId": top_paper.get("paperId", None)
        }
    
    return None

def get_references(paper_id):
    """Retrieve the list of references (citations used) in the given paper."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    params = {"fields": "references.title,references.authors,references.year,references.url"}
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Error: {response.status_code}, {response.text}"
    
    data = response.json()
    
    if "references" in data:
        return [
            {
                "title": ref.get("title", "Unknown"),
                "authors": [author["name"] for author in ref.get("authors", [])],
                "year": ref.get("year", "N/A"),
                "url": ref.get("url", "")
            }
            for ref in data["references"]
        ]
    
    return []

# Example usage
topic = "Gaussian Splatting"
most_relevant_paper = find_most_relevant_paper(topic)

if most_relevant_paper:
    print(f"Most Relevant Paper:\nTitle: {most_relevant_paper['title']}\nYear: {most_relevant_paper['year']}\nCitations: {most_relevant_paper['citationCount']}\nURL: {most_relevant_paper['url']}\n")
    
    # Retrieve references
    references = get_references(most_relevant_paper["paperId"])
    
    print("\nReferences (Citations Used in the Paper):")
    for ref in references[:5]:  # Show top 5 references
        print(f"Title: {ref['title']}\nAuthors: {', '.join(ref['authors'])}\nYear: {ref['year']}\nURL: {ref['url']}\n")
else:
    print("No relevant paper found.")
