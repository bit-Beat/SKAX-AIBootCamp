from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from typing import List

from langchain_openai import ChanOpenAI
from langchain_openai import OpenAIEmbeddings
import requests, json, os

from ai.rerank_class import DocumentScorer, SemanticRanker
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser

from ai.prompt.prompt import SYSTEM_PROMPT, SYSTEM_USER, AI_PROMPT, USER_PROMPT, SCORER_SYSTEM
from ai.state import QAState
from langchain.agents import Tool, AgentExecutor, create_react_agent
from ai.model.aimodels import llm, embeddings

# 검색한 문서 결과를 하나의 문단으로 합쳐줍니다.
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- helpers ---
def load_vector_store():
    #현행 RAG와 동일
    current_dir = os.path.dirname(os.path.abspath(__file__))
    loader = DirectoryLoader(current_dir+"/db", glob="**/*.txt", loader_cls=TextLoader) # 'db'폴더의 모든 텍스트 파일 로드
    docs = loader.load()
    split = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=100)
    chunks = split.split_documents(docs)
    return FAISS.from_documents(documents=chunks, embedding=embeddings)

# --- nodes ---
def parse_node(state: QAState) -> QAState:
    # 간단 카테고리 룰: 최신/브랜드/가격/매장/트렌드/뉴스 → 사용자 쿼리에서 검색이 필요한 키워드나 검색을 선호하는지 단어 추출
    q = state['qeustion']
    ai_bias = any(k in q for k in ['검색', '요즘', '트렌드', '브랜드', '가격', '원가', '매장', '판매', '구매', '뉴스'])
    state['route'] = "AI" if ai_bias else None
    return state

def retrieve_node(state: QAState) -> QAState:
    docs = RANKER.retrieve(state["question"]) # 상위4개 추출
    state['docs'] = docs
    state['context'] = format_docs(docs)
    return state

def answer_rag_node(state: QAState) -> QAstate: # RAG 기반 문서 답변 추출
    prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("user", SYSTEM_USER)])
    chain = prompt | llm | StrOutputParser()
    ans = chain.invoke({"question" : state['question'], 'context':state['context']})
    state['rag_answer'] = ans
    return state

def grade_node(state: QAState) -> QAState:
    # 간략 grader (필요시 별도 프롬프트로 정교화)
    grader = ChatPromptTemplate.from_messages([("system", SCORER_SYSTEM), ("user", SYSTEM_USER)])
    out = (grader | llm | StrOutputParser()).invoke({"question" : state["question"], "context":state["context"]})

    try :
        g = json.loads(out)
        state["relevance_score"] = float(g.get("relevance", 0.0))
        state['faithfulness'] =float(g.get("faithfulness", 0.0))
    except :
        state['relevance_score'] = 999
        state['faithfulness'] = 999

    if state.get('route') == 'ai':
        if state['relevance_score'] >= 0.8 and state['faithfulness'] >= 0.85 : # 이미 AI 바이어스라면 AI 우선, 다만 RAG가 매우 높으면 RAG 답변 유지
            state["route"] = "RAG"
        else:
            state["route"] = "AI"
    else:
        r, f = state["relevance_score"], state["faithfulness"]
        state["route"] = "RAG" if (r >= 0.7 and f >= 0.7) else "AI"

    return state

def ai_answer_node(state: QAState) -> QAState:
    prompt = ChatPromptTemplate.from_messages([("system", AI_PROMPT), ("user", USER_PROMPT)])
    chain = prompt | llm | StrOutputParser()
    ans = chain.invoke({"question" : state["question"]})
    state["ai_answer"] = ans
    return state

def finish_node(state: QAState) -> QAState:
    return state

# RAG Rerank 도출
VECTOR = load_vector_store()
SCORER = DocumentScorer(llm)
RANKER = SemanticRanker(VECTOR, SCORER)

# --- Graph Wiring ---
graph = StateGraph(QAState)
graph.add_node("parse", parse_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("answer_rag", answer_rag_node)
graph.add_node("grade", grade_node)
graph.add_node("answer_ai", ai_answer_node)
graph.add_node("finish", finish_node)

graph.set_entry_point("parse")
graph.add_edge("parse", "retrieve")
graph.add_edge("retrieve", "answer_rag")
graph.add_edge("answer_rag", "grade")

def router(state: QAState):
    r = state["route"]
    if r == "RAG":
        return "RAG"
    if r == "AI" :
        return "AI"
    return "RAG"

graph.add_conditional_edges(
    "grade",
    router,
    {
        "RAG" : END,
        "AI" : "answer_ai",
    },
    )
graph.add_edge("answer_ai", END)
app = graph.compile()











    
    
