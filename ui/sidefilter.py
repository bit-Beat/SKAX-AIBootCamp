import streamlit as st

def sidefilter():
    with st.sidebar:
        st.title(" 조건 필터")
        st.caption("조건을 적용하면 검색/추천 품질이 좋아져요.")
        use_time_toggle = st.toggle("조건활성화")
        st.session_state.filterTrigger = use_time_toggle

        situation = st.selectbox("상황", ["선택안함", "다이어트", "손님접대", "간단요리", "채식", "든든한 한 끼", "야식", "아이반찬", "해장"], index=0, disabled=not use_time_toggle)
        st.session_state.filters['situation'] = None if situation == "선택안함" else situation

        difficulty = st.selectbox("난이도", ["선택안함", "쉬움", "보통", "어려움"], index=0, disabled=not use_time_toggle)
        st.session_state.filters['difficulty'] = None if difficulty == "선택안함" else difficulty

        cooking_time = st.dlider("조리시간(분)", min_value=0, max_value=120, value=(0, 60), step=5, disabled=not use_time_toggle)
        st.session_state.filters['time'] = cooking_time

        diet = st.selectbox("식단", ['선택안함', '저탄수', '저지방', '고단백', '비건'], index=0, disabled=not use_time_toggle)
        st.session_state.filters['diet'] = None if diet == '선택안함' else diet

        allergies = st.multiselect("알레르기 재료", ["땅콩", "우유/유제품", "달걀", "밀/글루텐", "갑각류", "생선", "대두", "견과류", "기타", "참깨"], default=[], placeholder='중복선택 가능', disabled = not use_time_toggle)
        st.session_state.filters['allergies'] = allergies

        include_ings = st.text_input("포함할 재료(쉼표 구분)", placeholder="예) 닭가슴살, 브로콜리", disabled=not use_time_toggle)
        st.session_state.filters['include_ingredients'] = normalize_csv(include_ings)

        exclude_ings = st.test_input("제외할 재료(쉼표 구분)", placeholder="예) 마요네즈, 버터", disabled=not use_time_toggle)
        st.session_state.filters['exclude_ingredients'] = normalize_csv(exclude_ings)

        servings = st.number_input("인원 수", min_value=1, max_value=8, value=1, step=1, disabled=not use_time_toggle)
        st.session_state.filters['servings'] = servings

        st.divider()
        st.caption("필터는 검색 시 메타데이터 필터/리랭크에 활용됩니다.")

def normalize_csv(s):
    return [x.strip() for x in s.split(",") if x.strip()]
