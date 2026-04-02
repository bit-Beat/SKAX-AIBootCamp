# [SKAX]AI-BootCamp

🎯 주제 : 음식/레시피 Q&A AI 비서
🗓️ 과제 일정 : 7기 [2025.09.15 ~ 2025.10.17]

### Python Version
- Ver 3.11

### config 파일 설정
1. config.ini 파일에는 Azure Open AI API 세팅 값들을 입력 **개발을 위해 주어진 API Key로 사용**

### Streamlit 실행
1. streamlit run app.py

### 총 디렉토리 구조 (※ 아래 파일들은 해당 경로에 존재햐여야 함.)
root [dir📁]
┣━ README.md
┣━ **app.py**
┣━ requirements.txt
┣━ ui [dir📁]
┃  ┣━ chat_ui.py
┃  ┣━ init_state.py
┃  ┗━ sidefilter.py
┃
┗━ ai [dir📁]
   ┣━ db [dir📁]
   ┃  ┗━ sidefilter.py
   ┣━ model [dir📁]
   ┃  ┗━ aimodels.py
   ┃  ┗━ config.ini
   ┣━ prompt [dir📁]
   ┃  ┗━ prompt.py
   ┣━ call_llm.py
   ┣━ graph_multi_agent.py
   ┣━ rerank_class.py
   ┗━ state.py

### 파일 리스트 (※ 아래 파일들은 해당 경로에 존재햐여야 함.)
`[py 파일]`
- chat_ui.py : 사용자에게 출력할 메인 홈페이지 UI 파일
- init_state.py : Streamlit 세션 값 정의 파일
- sidefilter.py : 사이드 조건필터 UI
- aimodels.py : llm, embedding 모델 정의 파일
- prompt.py : llm 프롬프트 정의 파일
- call_llm.py : llm을 호출 후 결과를 리턴 하는 파일
- **graph_multi_agent.py** : RAG_LLM Agent 파이프라인 코어 파일
- rerank_class.py : ReRank 파이프라인 코어 클래스 파일
- state.py : LangGraph State 파일
- **app.py** (최종실행파일) : 테스트 코드를 생성해주는 최종 실행 파일

`[dataset 파일]`
- recipes.txt : LLM을 이용해 중복되지 않도록 다양한 레시피를 구조화하여 저장한 txt파일

`[ini 파일]`
- **config.ini** : Azure Open AI API 환경변수 세팅 파일

### 전체적 프로세스 흐름도
사용자입력(query) → query 전달 → query split → FAISS Vector Store → Query와 유사한 문서 16개 탐색 → LLM이 16개 문서 유사도 측정 → 상위 4개 문서 추출 → 상위4개문서 + Query 기반으로 LLM 답변 추출 → LLM이 질문과 상위 4개 문서가 서로 유의미한지 판단 → 유의미하지 않으면 LLM 자유생성 답변 생성 → 유의미하면 전에 추출했던 답변 그대로 출력

### 과제 개요
	1. 과제 선정 배경 및 목적 
		- 1인 가구의 증가, 건강에 대한 관심 확대, 다양한 식문화의 확산 등으로 인해 음식/요리에 대한 정보 탐색 수요가 증가함에 따라 사용자가 원하는 정보를 쉽고 빠르게 찾기 어렵다는 한계를 극복하고자 음식, 레시피, 재료 활용법 등에 대해 신속하고 정확하게 답변해주는 음식/레시피 Q&A AI 비서를 개발하는 것을 목표로 합니다.
	2. 서비스 개요
		- 음식/레시피 Q&A AI 비서는 사용자가 입력하는 다양한 질문(예: 이 요리의 대체 재료는? 다이어트에 좋은 저녁 메뉴 추천 등)에 대해, RAG(Retrieval-Augmented Generation) 기법을 활용하여 신뢰성 높은 레시피 데이터와 요리 관련 문서를 참조해 맞춤형 답변을 제공합니다.
		- 사용자는 음식 이름, 재료, 상황(예: 다이어트, 손님 접대, 간단한 요리 등), 조리 시간, 난이도 등 다양한 조건을 입력할 수 있으며, AI 비서는 이에 맞는 레시피 추천, 대체 재료 안내, 조리 팁, 영양 정보 등 실질적으로 도움이 되는 정보를 제공합니다.
		- 주요기능 : 음식/재료/상황별 맞춤 레시피 추천, 대체 재료, 조리 팁, 영양정보 안내 등, 요리 난이도, 조리시간 조건별 필터링, Streamlit 기반 직관적 인터페이스 제공

### 과제 전략
	1. 기술적 접근 방법
			· RAG(retrieval-Augmented Generation) 기법 활용
				- 정제된 레시피, 요리 팁, 영양 정보 등 다양한 문서를 수집 및 전처리 하여 벡터 데이터베이스 (FAISS)
				- 사용자의 질문을 임베딩하여 관련 문서를 검색(Retrieval)하고, 검색된 정보를 바탕으로 AI가 답변을 생성(Generation)
			· 데이터 구성 및 전처리
				- 오픈 레시피 데이터셋, 요리 블로그, 식품 영양 정보 등 다양한 출처의 데이터를 수집
				- 중복, 오류, 불필요한 정보를 제거, 일관된 포맷으로 정제
			· 벡터 DB 활용
				- FAISS를 활용하여 대용량의 레시피/요리 정보를 효율적으로 검색

	2. AI Agent 설계
			· 프롬프트 엔지니어링 전략
				- Role 부여, Few-shot Prompting 등 다양한 프롬프트 기법 적용
	3. UI/UX 구현
			· Streamlit 기반 인터페이스 설계
				- 사용자가 질문을 입력하고, AI가 답변을 제공하는 대화형 UI 구현
				- 레시피, 재료, 영양 정보 등은 표, 리스트, 이미지 등으로 시각화

###기대효과/활용방안
- 요리/초보자부터 숙련자까지 누구나 쉽고 빠르게 음식/레시피 정보를 얻을 수 있음.
- 음식/레시피 관련 정보 탐색의 효율성 및 정확성 향상
- 건강식, 다이어트, 알레르기 등 다양한 상황에 맞는 맞춤형 정보 제공
- 실제 서비스로 확장 시, 식품 유통, 레시피 를랫폼, 건강관리 서비스 등 다양한 비즈니스 분야에 적용 가능
   
