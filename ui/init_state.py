import streamlit as st

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role" : "assistant",
            "content" : "안녕하세요! 레시피 지식 기반 RAG로 답변하는 **음식/레시피 Q&A AI 비서**입니다. \n\n - 좌측 사이드바에서 *상황/난이도/조리시간/알레르기/재료* 조건을 고르면 더 맞춤 추천이 가능해요. \n - 아래 채팅창에 궁금한 레시피나 추천 메뉴를 질문해 보세요!",
            "meta" : {}
            }]

    if 'filters' not in st.session_state:
        st.session_state.filters = {
            'situation':None, # 상황 : 다이어트/손님접대/간단요리 등등
            'difficulty':None, # 난이도 : 쉬움, 보통, 어려움
            'time' : (0, 120), # 조리시간(분) 범위
            'diet' : None, #다이어트 식단 선택
            'allergies' : [], # 알레르기 회피 재료
            'include_ingredients' : [], # 포함할 재료
            'exclude_ingredients' : [], # 제외할 재료
            'servings': (1, 8) # 인원수 범위
            }

    if 'filterTrigger' not in st.session_state:
        st.session_state.filterTrigger = False
