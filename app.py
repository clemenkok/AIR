import streamlit as st
import json
from collections import defaultdict
from knowledge_graph import find_most_relevant_paper, build_graph, plot_citation_graph_streamlit
from code_execution import fetch_code_snippet, display_code_ide

st.title("Knowledge Graph Viewer")

knowledge_graph = defaultdict(list)
topic = st.text_input("Enter a research topic:", "Gaussian Splatting")

graph_generated = False
if st.button("Generate Graph"):
    most_relevant_paper = find_most_relevant_paper(topic)
    print(most_relevant_paper.name)
    build_graph(knowledge_graph, most_relevant_paper, depth=3)
    print(json.dumps(knowledge_graph))
    st.write("Knowledge Graph Built:", knowledge_graph)
    plot_citation_graph_streamlit(knowledge_graph)
    graph_generated = True

if graph_generated:
    code_snippet = fetch_code_snippet()
    display_code_ide(code_snippet)
