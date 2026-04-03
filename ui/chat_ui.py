import streamlit as st
import time
from ai.call_llm import call_rag

def main_page():
    st.title("🍟🍳🍗음식/레시피 Q&A AI 챗봇")
    st.info("사용자의 검색 정보는 외부로 유출되지 않습니다.", icon = "💡")
    st.write("")
    st.markdown("레시피 지식 기반을 활용하여 질문에 답변합니다. 원하시는 요리나 재료에 대해 질문해 보세요.\n")

    st.markdown("#### ✨ 조건 필터에 맞춰서 빠르게 메뉴를 추천받아보세요!")
    quick_input = " 조건 필터에 맞는 메뉴를 추천 해주세요."
    if st.button("빠른 검색", icon="⚡"):
        if not st.session_state.filterTrigger:
            st.warnings("먼저 좌측 필터를 활성화하여 시도해주세요.", icon="⚠️")
        else :
            append_user_message(quick_input)
            with st.spinner("레시피 지식 검색 및 답변 생성 중..."):
                summary_text = call_rag(quick_input, st.session_state.filters, st.session_state.filterTrigger) # RAG LLM 호출
                append_assistant_messages(summary_text)

    st.divider()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            render_recipe_card(msg['content'])

    user_input = st.chat_input("어떤 음식이나 레시피가 궁금하신가요? (예: 다이어트 메뉴 추천 등)")
    
    
    if user_input :
        append_user_message(user_input)

        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("레시피 지식 검색 및 답변 생성 중..."):
                summary_text = call_rag(user_ilnput, st.session_state.filters, st.session_state.filterTrigger) # RAG LLM 호출
                render_recipe_card(summary_text)
                append_assistant_messages(summary_text)

def render_recipe_card(summary:str):
    st.markdown(summary)
    st.divider()

def append_user_message(content):
    st.session_state.messages.append({"role":"user", "content":content, "meta":{}})

def append_assistant_messages(summary_text: str):
    st.session_state.messages.append({"role":"assistant", "content":summary_text, "meta":{"type":"card"}})






                
