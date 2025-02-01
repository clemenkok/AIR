import requests
from collections import defaultdict
import networkx as nx
from pyvis.network import Network
import streamlit as st
import json

import matplotlib.pyplot as plt
from datatypes import Node
from semantic_scholar import find_most_relevant_paper, get_influential_papers

# Semantic Scholar API endpoint
BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

def build_graph(knowledge_graph: dict, start_node: Node, depth: int = 3):
    if depth == 0:
        return

    if start_node:
        references: list[Node] = get_influential_papers(start_node.paper_id)

        for ref in references:
            key = str(start_node) # Convert Node to a string key
            if key not in knowledge_graph:
                knowledge_graph[key] = []
            knowledge_graph[key].append(str(ref))  # Store reference names instead of Node objects
            build_graph(knowledge_graph, ref, depth - 1)


def plot_citation_graph_streamlit(citation_dict):
    """
    Displays a citation graph using Pyvis inside Streamlit.
    """
    G = nx.DiGraph()
    
    for paper, citations in citation_dict.items():
        for cited_paper in citations:
            G.add_edge(str(paper), str(cited_paper))
    
    net = Network(notebook=False, directed=True)
    
    # Configure the network to hide node info
    net.set_options("""
        var options = {
            "nodes": {
                "font": {
                    "size": 12
                }
            },
            "edges": {
                "color": {
                    "inherit": true
                },
                "smooth": false
            },
            "physics": {
                "forceAtlas2Based": {
                    "gravitationalConstant": -50,
                    "springLength": 100
                },
                "minVelocity": 0.75,
                "solver": "forceAtlas2Based"
            }
        }
    """)
    
    for node in G.nodes:
        net.add_node(node, label=node, title=node)  # title will show on hover
    
    for edge in G.edges:
        net.add_edge(edge[0], edge[1])
    
    html_path = "citation_graph.html"
    net.write_html(html_path)

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    st.components.v1.html(html_content, height=600)



# Streamlit UI
st.title("Knowledge Graph")

knowledge_graph = defaultdict(list)
topic = st.text_input("Enter a research topic:", "Gaussian Splatting")

if st.button("Generate Graph"):
    most_relevant_paper = find_most_relevant_paper(topic)
    print(most_relevant_paper.name)
    build_graph(knowledge_graph, most_relevant_paper, depth=3)
    print(json.dumps(knowledge_graph))
    st.write("Knowledge Graph Built:", knowledge_graph)
    plot_citation_graph_streamlit(knowledge_graph)
