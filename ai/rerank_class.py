from typing import List
from langchain.schema import Document
from ai.prompt.prompt import RERANK_PROMPT
from langchain_core.prompts import PromptTemplate

import json

class DocumentScorer:
    def __init__(self, llm):
        self.llm = llm

    def evaluate_document(self, query: str, content: str) -> float: # LLM을 사용해 문서와 쿼리간의 의미적 관련성을 1~10점으로 평가
        try:
            prompt = PromptTemplate.from_template(RERANK_PROMPT)
            formatted = prompt.format(query = query, content=content)
            response = self.llm.invoke(formatted) # LLM에 프롬프트를 전송하고 JSON 형식의 응답을 받음

            score = json.loads(response.content.strip().replace('`', '').replace('json', ''))["relevance_score"] # 응답에서 relevance_score 값을 추출, 혹시 출력된 기타 문자들은 모두 제거 후 json 값 추출
            return float(score) # 점수를 float으로 변환하여 반환
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return 5.0 # 에러 발생 시 중간 점수로 처리하여 시스템 안정성 유지
        
    def postprocess_documents(self, documents: List[Document], query: str) -> List[Document]:
        scored_docs = []
        for index, doc in enumerate(documents):
            content = doc.page_content # 현재 처리 중인 문서에서 순수 텍스트 컨텐츠만 추출
            score = self.evaluate_document(query, content) # LLM으로 문서 관련성 점수 계산 (1 ~ 10 사이 점수)
            scored_docs.append((doc, score)) # 현재 문서와 계산된 점수를 튜플로 저장

        # 모든 문서를 점수 기준 내림차순으로 정렬하고 상위 4개만 선택하여 반환
        ranked_docs = sorted(scored_docs, key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in ranked_docs[:4]]

# 벡터 검색 결과에 LLM 기반 의미적 평가를 적용하여 최적의 문서를 선별하는 시스템
class SemanticRanker:
    def __init__(self, vector_store, scorer): # 생성자에서 벡터 검색용 저장소와 LLM 기반 문서 평가기 인스턴스를 받아 저장
        self.vector_store = vector_store # 벡터 검색용 저장소
        self.scorer = scorer # LLM 기반 문서 평가기

    def retrieve(self, query: str) -> List[Document]:
        vector_results = self.vector_store.similarity_search(query, k=16) # 벡터 검색으로 유사도 기반 후보 문서 16개를 추출하고 LLM으로 재평가
        reranked_results = self.scorer.postprocess_documents(vector_results, query) # LLM 으로 문서들을 재평가하고 재정렬하여 최적의 4개 선택
        return reranked_results







    
    
            
            
