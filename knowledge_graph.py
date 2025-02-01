import requests
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
import streamlit as st

from datatypes import Node
from semantic_scholar import find_most_relevant_paper, get_influential_papers

# Semantic Scholar API endpoint
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def get_references(paper_id: str):
    """Retrieve the list of references (citations used) in the given paper."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}"
    params = {"fields": "references.title,references.authors,references.year,references.url"}
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"Error: {response.status_code}, {response.text}"
    
    data = response.json()
    
    if "references" in data:
        references = [
            {
                "title": ref.get("title", "Unknown"),
                "authors": [author["name"] for author in ref.get("authors", [])],
                "year": ref.get("year", "N/A"),
                "url": ref.get("url", ""),
                "citationCount": ref.get("citationCount", 0)
            }
            for ref in data["references"]
        ]
        
        references_sorted = sorted(references, key=lambda x: x["citationCount"], reverse=True)
        return references_sorted[:5]  # Return top 5 references
    
    return []

def build_graph(knowledge_graph: dict, start_node: Node, depth: int = 3):
    if depth == 0:
        return

    if start_node:
        references: list[Node] = get_influential_papers(start_node.paper_id)
        for ref in references:
            knowledge_graph[start_node].append(ref)
            build_graph(knowledge_graph, ref, depth - 1)

def plot_citation_graph_streamlit(citation_dict):
    """
    Displays a citation graph using Pyvis inside Streamlit.
    """
    G = nx.DiGraph()
    
    for paper, citations in citation_dict.items():
        for cited_paper in citations:
            G.add_edge(paper.name, cited_paper.name)
    
    net = Network(notebook=False, directed=True)
    for node in G.nodes:
        net.add_node(node, label=node)
    
    for edge in G.edges:
        net.add_edge(edge[0], edge[1])
    
    # Save the file in a Streamlit-friendly temporary directory
    html_path = "citation_graph.html"
    net.write_html(html_path)

    # Display in Streamlit
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    st.components.v1.html(html_content, height=600)


# Streamlit UI
st.title("Citation Graph Viewer")

knowledge_graph = defaultdict(list)
topic = st.text_input("Enter a research topic:", "Gaussian Splatting")

if st.button("Generate Graph"):
    most_relevant_paper = find_most_relevant_paper(topic)
    build_graph(knowledge_graph, most_relevant_paper, depth=3)
    st.write("Knowledge Graph Built:", knowledge_graph)
    plot_citation_graph_streamlit(knowledge_graph)
