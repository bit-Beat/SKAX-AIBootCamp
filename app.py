import streamlit as st
from ui.chat_ui import main_page
from ui.init_state import init_session_state
from ui.sidefilter import sidefilter

st.set_page_config(page_title="음식/레시피 Q&A AI 챗봇", page_icon="🥩")

if __name__ == "__main__":
    init_session_state() # UI Session Initialize
    sidefilter() # SideFilter UI Initialize
    main_page() # Main Page UI Initialize
