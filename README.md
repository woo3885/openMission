# RAG Q&A Bot with LangChain

2주 해커톤 프로젝트: LangChain을 사용한 RAG(검색 증강 생성) Q&A 봇

## 기술 스택
- **Web Framework:** FastAPI
- **LLM:** GPT-4o (OpenAI)
- **Embedding:** OpenAI Embeddings
- **Orchestration:** LangChain (LCEL)
- **Vector Store:** ChromaDB
- **Document Loader:** PyPDF

## 설치 및 실행

### 1. 환경 설정
```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 라이브러리 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일에 실제 OPENAI_API_KEY 입력
```

### 2. 데이터 준비
```bash
# document.pdf 파일을 프로젝트 루트에 배치
# 임베딩 및 벡터 DB 생성
python ingest.py
```

### 3. 서버 실행
```bash
python main.py
# 또는
uvicorn main:app --reload
```

서버가 실행되면:
- API: http://localhost:8000
- 문서: http://localhost:8000/docs

## 프로젝트 구조
```
.
├── main.py              # FastAPI 서버 및 RAG 체인
├── ingest.py            # 데이터 임베딩 스크립트
├── requirements.txt     # 의존성
├── .env                 # 환경변수 (gitignore)
├── document.pdf         # 학습할 문서
└── db/                  # 벡터 DB (gitignore)
```

## API 사용법
```bash
# 질문하기
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "문서에 대한 질문"}'
```
