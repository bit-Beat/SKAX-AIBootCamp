from ai.graph_multi_agent import app

def call_rag(user_query: str, filters: dict, filterTrigger: bool):
    filter_txt = "조건필터 : " + ",".join([f"{k}:{v}" for k, v in filters.items()]) if filterTrigger else "사용자가 선택한 조건 없음"
    question = filter_txt + " " + user_query

    init = {
        "question" : question,
        "filters" : filters if filterTrigger else {},
        "docs" : [],
        "context" : "",
        "rag_answer" : None,
        "ai_answer" : None,
        "route" : None,
        "relevance_score" : None,
        "faithfulness": None
    }
    final_state = app.invoke(init)
    answer = final_state.get("ai_answer") or final_state.get("rag_answer") # 우선순위 : ai > rag (ai를 탔으면 ai) 아니면 rag

    return answer
    
