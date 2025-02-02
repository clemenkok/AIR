import requests
import streamlit as st

from constants import BACKEND_URL

# st.set_page_config(layout="wide")
st.session_state.streamed_text = ""

def experiment_outline_frontend():
    st.session_state.setdefault('streamed_text', "")

    # Custom CSS for height and button positioning
    st.markdown("""
        <style>
            .text-area {
                height: 70vh !important;
            }
            # .stButton {
            #     display: flex;
            #     justify-content: center;
            # }
            .stButton > button {
                padding: 0.5em 2em;
                font-size: 1.2rem;
                min-width: 150px;
                transition: all 0.2s ease;
            }
            .stButton > button:hover {
                transform: scale(1.05);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("#### Experiment Outline")

    # Text Area with streamed content
    st.text_area(
        label="Outline",
        value=st.session_state.streamed_text,
        placeholder="Thinking of ideas...",
        key="outline_text",
        height=500  # Base height to ensure the text_area expands
    )

    # _, regen_btn, _, cont_btn, _ = st.columns([5, 4, 1, 4, 5])

    # with regen_btn:
    if st.button("Regenerate"):
        stream_claude_section("Regenerate")

    # with cont_btn:
    if st.button("Continue"):
        st.session_state.experiment_outline_complete = True
        # print(st.session_state.experiment_outline_complete)
        
def stream_claude_section(section_text):
    # Populate the arg
    return

    # Reset the streamed text
    st.session_state.streamed_text = ""

    # Replace this with your actual Claude streaming API endpoint
    url = f"{BACKEND_URL}/generate_code"  # Example endpoint
    
    response = requests.post(url, json={"plan": section_text}, stream=True)
    
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                st.session_state.streamed_text += decoded_line
    else:
        st.error("Error: Unable to stream from Claude API.")

# outline()