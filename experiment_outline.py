import streamlit as st

st.set_page_config(layout="wide")

text = "Abu ali"


def outline():
    st.markdown("#### Experiment Outline")
    st.text_area("Outline", f"{text}")

    return

outline()