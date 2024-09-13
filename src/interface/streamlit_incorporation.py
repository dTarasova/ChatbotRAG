import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

def setup_streamlit():
    
    st.set_page_config(
        page_title="Requirements Engineering Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="auto",
    )

    nav = get_nav_from_toml(
        "src/interface/.streamlit/pages.toml"
    )

    pg = st.navigation(nav)

    add_page_title(pg)

    pg.run()
