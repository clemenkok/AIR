import streamlit as st

st.set_page_config(layout="wide")

from knowledge_graph import knowledge_graph_frontend
from experiment_outline import experiment_outline_frontend
from code_execution import code_execution_frontend

if __name__ == "__main__":
    st.session_state.knowledge_graph_complete = False
    st.session_state.experiment_outline_complete = False
    st.session_state.code_execution_complete = False

    knowledge_graph_frontend()

    if st.session_state.knowledge_graph_complete:
        experiment_outline_frontend()
        if st.session_state.experiment_outline_complete:
            code_execution_frontend()
