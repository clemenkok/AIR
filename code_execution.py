import streamlit as st
import sys
import io

# set width of page to be full 
st.set_page_config(layout="wide")

def fetch_code_snippet():
    return """def factorial(n):
    return 1 if n == 0 else n * factorial(n-1)

print(factorial(5))"""

def execute_code(code):
    """Executes the given Python code and captures the output."""
    output_buffer = io.StringIO()
    try:
        sys.stdout = output_buffer  # Redirect stdout to capture print statements
        exec(code, {})  # Execute code in an isolated environment
    except Exception as e:
        return f"Error: {e}"
    finally:
        sys.stdout = sys.__stdout__  # Reset stdout
    
    return output_buffer.getvalue()

def display_code_ide(code):
    st.markdown("## Code Execution")

    st.markdown("""
        <style>
            .stColumns {
                display: flex;
                align-items: stretch;  /* Makes columns the same height */
            }
            .code-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .code-header h4 {
                margin: 0;
            }
            .stButton {
                display: flex;
                justify-content: center;
            }
            .stButton > button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                cursor: pointer;
                border-radius: 5px;
                font-size: 14px;
            }
            .stButton > button:hover {
                background-color: #45a049;
            }
            .button-container {
                display: flex;
                justify-content: flex-end;  /* Right-aligns the button */
            }
            /* Set st.code height equal to st.text_area */
            .stCodeBlock {
                height: 400px !important;
                overflow-y: auto;
            }
            pre {
                height: 50vh !important;
                overflow-y: auto;  /* Enable scrolling inside the code block */
            }
            /* Remove extra padding/margin above the text area */
            textarea, .stTextArea label {
                margin-top: 0px !important;
                padding-top: 0px !important;
            }
            .stTextArea label {
                display: none;  /* Completely hide any label above the text area */
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Ensure session state variable is initialized
    if "code_output" not in st.session_state:
        st.session_state["code_output"] = ""
    
    container = st.container()
    with container:
        col1, col2 = st.columns([1, 1])  # Adjust column width for better layout
        
        with col1:
            st.markdown("""
                <div class="code-header">
                    <h4>Code:</h4>
                </div>
            """, unsafe_allow_html=True)

            st.code(code, language="python", line_numbers=True)
            if st.button("Run Code"):
                # Replace this with your actual function to execute code
                st.session_state["code_output"] = execute_code(code)
        
        with col2:
            st.markdown("#### Output:")
            st.text_area("", st.session_state.get("code_output", ""), height=400, label_visibility="collapsed")

    return

def display_images():
    # List of image filenames
    image_urls = [
        "lossfunction.png",
        "lossfunction.png",
        "lossfunction.png",
        "lossfunction.png",
        "lossfunction.png"
    ]

    st.markdown("## Images:")
    num_images = len(image_urls)
    num_columns_per_row = 3

    for i in range(0, num_images, num_columns_per_row):
        cols = st.columns(num_columns_per_row)
        for j in range(num_columns_per_row):
            if i + j < num_images:
                with cols[j]:
                    st.image(image_urls[i + j], width=400)

st.title("Knowledge Graph Viewer")
code_snippet = fetch_code_snippet()
display_code_ide(code_snippet)
display_images()
