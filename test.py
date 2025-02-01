
import feedparser
import requests

def search_arxiv(query, max_results=10):
    base_url = "http://export.arxiv.org/api/query?"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    
    # Make request
    response = requests.get(base_url, params=params)
    
    # Parse response
    feed = feedparser.parse(response.text)
    
    # Extract papers
    papers = []
    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "authors": [author.name for author in entry.authors],
            "summary": entry.summary,
            "published": entry.published,
            "link": entry.link
        })
    
    return papers

# Example usage
papers = search_arxiv("Gaussian Splatting", max_results=5)
for p in papers:
    print(f"Title: {p['title']}\nAuthors: {', '.join(p['authors'])}\nDate: {p['published']}\nLink: {p['link']}\n")
