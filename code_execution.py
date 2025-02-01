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
    
    # Ensure session state variable is initialized
    if "code_output" not in st.session_state:
        st.session_state["code_output"] = ""
    
    container = st.container()
    with container:
        col1, col2 = st.columns([1, 1])  # Adjust column width for better layout
        
        with col1:
            st.markdown("#### Code:")
            st.code(code, language="python", line_numbers=True)
            if st.button("Run Code"):
                st.session_state["code_output"] = execute_code(code)
        
        with col2:
            st.markdown("#### Output:")
            st.text_area("", st.session_state["code_output"], height=400)


st.title("Knowledge Graph Viewer")
code_snippet = fetch_code_snippet()
display_code_ide(code_snippet)
