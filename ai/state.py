from typing import TypedDict, List, Literal, Optional
from langchain.schema import Document

class QAState(TypedDict):
    question: str                           # 사용자 질문
    filters: Optional[dict]                 # 사용자 조건 검색
    docs = List[Document]                   # 벡터+리랭크 상위 N개 문서
    context: str                            # format_docs (문서 포매팅) 결과
    rag_answer: Optional[str]               # RAG 문서 기반의 답변 결과
    ai_answer: Optional[str]                # AI가 자유생성한 답변
    route: Optional[Literal["RAG", "AI"]]   # RAG or AI
    relevance_score: Optional[float]        # LLM/리랭크/그레이더 종합 점수 (0~1)
    faithfulness: Optional[float]           # 답변이 컨텍스트/출처에 얼마나 충실한지 (0~1)
