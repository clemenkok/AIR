import requests
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx

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
        
        # Sort references by citation count in descending order
        references_sorted = sorted(references, key=lambda x: x["citationCount"], reverse=True)

        # Return top 5 references
        return references_sorted[:5]
    
    return []

def build_graph(knowledge_graph: dict, topic: str, depth: int = 1):
    if depth == 0:
        return

    most_relevant_paper: Node = find_most_relevant_paper(topic)
    if most_relevant_paper:
        references: list[Node] = get_influential_papers(most_relevant_paper.paper_id)

        for ref in references:
            knowledge_graph[most_relevant_paper].append(ref)
            build_graph(knowledge_graph, ref.name, depth - 1)

def plot_citation_graph(citation_dict):
    """
    Plots a directed graph where nodes are paper titles, and edges represent citations.
    
    Args:
    citation_dict (dict): A dictionary where keys are paper titles and values are lists of cited paper titles.
    """
    # Create a directed graph
    G = nx.DiGraph()

    # Add edges from the dictionary
    for paper, citations in citation_dict.items():
        for cited_paper in citations:
            G.add_edge(paper.name, cited_paper.name)
    
    # Set figure size
    plt.figure(figsize=(12, 8))
    
    # Use spring layout for better visualization
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='skyblue', edgecolors='black')
    
    # Draw edges with arrows
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color='gray', width=1.5)
    
    # Add labels with smaller font size for clarity
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black', font_weight='bold')
    
    # Remove axis
    plt.axis('off')
    
    # Add title
    plt.title("Citation Graph", fontsize=15)
    
    # Show the plot
    plt.show()

def prune_graph(graph, iterations):
    for i in range(0, iterations):
        degree_map = defaultdict(int)

        for node in graph:
            for endpoint in graph[node]:
                print(endpoint)
                degree_map[endpoint] += 1
        leaves = [node for node in graph if degree_map[node] == 1]
        for node in graph:
            current_edges = graph[node]
            graph[node] = [item for item in current_edges if item not in leaves]
        for leaf in leaves:
            del graph[leaf]
    

if __name__ == "__main__":
    knowledge_graph = defaultdict(list)
    # knowledge_graph = {
    #     Node("Gaussian Splatting for Real-Time Radiance Field Rendering"): [
    #         Node("Neural Radiance Fields (NeRF)"), 
    #         Node("Instant Neural Graphics Primitives"), 
    #         Node("Volumetric Scene Representations")
    #     ],
    #     Node("Neural Radiance Fields (NeRF)"): [
    #         Node("Volume Rendering Techniques"), 
    #         Node("Photorealistic Scene Reconstruction")
    #     ],
    #     Node("Instant Neural Graphics Primitives"): [
    #         Node("Efficient 3D Scene Representations")
    #     ]
    # }

    topic = "Gaussian Splatting"
    most_relevant_paper = find_most_relevant_paper(topic)
    build_graph(knowledge_graph, topic)
    # print(knowledge_graph)
    plot_citation_graph(knowledge_graph)

    pruned_graph = knowledge_graph.copy()
    prune_graph(pruned_graph, 1)
    plot_citation_graph(pruned_graph)