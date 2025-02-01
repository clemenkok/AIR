import streamlit as st
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def fetch_code_snippet():
    # response = requests.get("https://api.example.com/get_code")  # Replace with actual API
    # if response.status_code == 200:
    #     return response.json().get("code", "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)\n\nprint(factorial(5))")
    return "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)\n\nprint(factorial(5))"

def display_code_ide(code):
    formatted_code = highlight(code, PythonLexer(), HtmlFormatter(style="monokai", full=True))
    st.markdown("## Code Execution")
    
    container = st.container()
    with container:
        col1, col2 = st.columns([2, 3])
        
        with col1:
            st.markdown("#### Code:")
            st.code(code, language="python", line_numbers=True)
            if st.button("Run Code"):
                st.session_state["code_output"] = "Error executing code"
        
        with col2:
            st.markdown("#### Output:")
            st.text_area("", st.session_state.get("code_output", ""), height=400)
    
    return
