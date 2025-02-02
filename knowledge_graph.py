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

def build_graph(knowledge_graph: dict, start_node: Node, depth: int = 3, node_metadata=None):
    """
    Recursively builds a citation graph up to the specified depth.
    Also populates a node_metadata dictionary with extra info (e.g. author, year).
    """
    print("Building graph")

    if depth == 0:
        return

    references = get_influential_papers(start_node.paper_id)

    # Store metadata for the starting paper
    if node_metadata is not None and str(start_node) not in node_metadata:
        node_metadata[str(start_node)] = {
            "title": start_node.name,
            "author": start_node.authors,
            "abstract": start_node.abstract,
            "year": str(start_node.year) if hasattr(start_node, "year") else "N/A"
        }

    for ref in references:
        key = str(start_node)
        if key not in knowledge_graph:
            knowledge_graph[key] = []

        knowledge_graph[key].append(str(ref))

        # Store metadata for the reference
        if node_metadata is not None and str(ref) not in node_metadata:
            node_metadata[str(ref)] = {
                "title": ref.name,
                "author": ref.authors,
                "abstract": ref.abstract,
                "year": str(ref.year) if hasattr(ref, "year") else "N/A"
            }

        # Recursively build the graph for the reference
        build_graph(knowledge_graph, ref, depth - 1, node_metadata)

def plot_citation_graph_streamlit(citation_dict, node_metadata):
    """
    Displays a citation graph using PyVis inside Streamlit with
    author name and year on hover.
    """
    print("Plotting
         graph")
    G = nx.DiGraph()

    # Add edges to the NetworkX graph
    for paper, citations in citation_dict.items():
        G.add_node(paper)
        for cited_paper in citations:
            G.add_node(cited_paper)
            G.add_edge(paper, cited_paper)

    # Create a PyVis network
    net = Network(notebook=False, directed=True)

    # Configure the network for better visuals
    net.set_options("""
        var options = {
          "nodes": {
            "shape": "dot",
            "size": 40,
            "font": {
                "size": 14,
                "face": "arial",
                "multi": true,
                "align": "center"
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

    # Add nodes with hover info
    for node in G.nodes:
        meta = node_metadata.get(node, {})
        title_text = meta.get("title", node)
        author = meta.get("author", "Unknown")
        abstract = meta.get("abstract", "Unknown")
        year = meta.get("year", "Unknown")

        # We'll display a shorter label so it doesn't crowd the graph
        label = f"{title_text[:30]}..." if len(title_text) > 30 else title_text

        # Full details on hover
        hover_text = f"{title_text}\nAuthor: {author}\nYear: {year}\nAbstract:{abstract}\n"
        net.add_node(node, label=label, title=hover_text)

    # Add edges
    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    # Generate the interactive graph HTML
    html_path = "citation_graph.html"
    net.write_html(html_path)

    # Render the graph in Streamlit
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    st.components.v1.html(html_content, height=600)

# Streamlit UI
st.title("Knowledge Graph")

# Instead of printing the JSON or dictionary above the graph, we store it silently.
knowledge_graph = defaultdict(list)
node_metadata = {}

topic = st.text_input("Enter a research topic:", "Gaussian Splatting")

if st.button("Generate Graph"):
    # Find the most relevant paper for the given topic
    most_relevant_paper = find_most_relevant_paper(topic)

    # Build the citation graph (up to depth=3)
    build_graph(knowledge_graph, most_relevant_paper, depth=3, node_metadata=node_metadata)

    # Optionally, if you still want to show the JSON, use an expander:
    # with st.expander("Show Raw Citation Data"):
    #     st.json(knowledge_graph)

    # Plot the graph with PyVis
    plot_citation_graph_streamlit(knowledge_graph, node_metadata)

# # # Streamlit UI
# st.title("Knowledge Graph")

# knowledge_graph = defaultdict(list)
# topic = st.text_input("Enter a research topic:", "Gaussian Splatting")

# if st.button("Generate Graph"):
#     most_relevant_paper = find_most_relevant_paper(topic)
#     print(most_relevant_paper.name)
#     build_graph(knowledge_graph, most_relevant_paper, depth=3)
#     print(json.dumps(knowledge_graph))
#     st.write("Knowledge Graph Built:", knowledge_graph)
#     plot_citation_graph_streamlit(knowledge_graph)
