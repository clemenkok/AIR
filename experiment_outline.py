import streamlit as st
from constants import BACKEND_URL
from claude2 import generate_outline

def experiment_outline_frontend():
    st.markdown("#### Experiment Outline")
    
    # Create a container for our streaming output
    output_container = st.empty()
    
    # Initialize session state if needed
    if 'streamed_outline' not in st.session_state:
        st.session_state.streamed_outline = ""

    # Init the streamed content
    stream_content(output_container)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regenerate", type="primary"):
            # Reset content
            st.session_state.streamed_outline = ""
            stream_content(output_container)
            
    with col2:
        if st.button("Continue"):
            st.session_state.experiment_outline_complete = True

def stream_content(container):
    """Handle the streaming with proper session state management"""
    payload = st.session_state.selected_paper_data
    
    def content_generator():
        try:
            for outline_content in generate_outline(payload):
                st.session_state.streamed_outline += outline_content

                yield outline_content
        except Exception as e:
            yield f"🚨 Connection error: {str(e)}"
    
    # Clear previous content and stream new response
    with container:
        st.session_state.streamed_outline = ""  # Clear previous content
        st.write(content_generator())