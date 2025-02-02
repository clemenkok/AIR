import streamlit as st
import json
from collections import defaultdict
from knowledge_graph import find_most_relevant_paper, build_graph, plot_citation_graph_streamlit
from code_execution import fetch_code_snippet, display_code_ide


def add_generated_section(graph, state):
    # generate text
    text = "hello world"
    st.write(text)
    st.divider()

    if st.buton("Regenerate plan"):
        add_generated_section(graph)
        pass
    
    if st.button("Continue to code"):
        # save state
        
        pass
