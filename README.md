# LangChain Chatbot with RAG & Gemini

2주 해커톤 프로젝트: LangChain을 활용한 GUI 챗봇 & RAG Q&A 봇

## 🎯 프로젝트 개요

이 프로젝트는 두 가지 방식의 AI 챗봇을 제공합니다:

1. **GUI 챗봇** (`chat_app.py`): Gemini API를 사용한 독립 실행형 데스크톱 챗봇
2. **RAG Q&A 봇** (`main.py`): 문서 기반 질의응답 FastAPI 서버

## 기술 스택
- **GUI Framework:** Tkinter
- **LLM:** Gemini Pro (Google), GPT-4o (OpenAI)
- **Embedding:** OpenAI Embeddings
- **Orchestration:** LangChain (LCEL)
- **Vector Store:** ChromaDB
- **Web Framework:** FastAPI

---

## 🤖 GUI 챗봇 (Gemini)

### 특징
- ChatGPT와 유사한 UI/UX
- Gemini Pro API 기반 대화
- 독립 실행형 데스크톱 애플리케이션
- 대화 히스토리 유지

### 실행 방법

#### 1. 환경 설정
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 라이브러리 설치
pip install -r requirements.txt
```

#### 2. API 키 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일에 Gemini API 키 추가
GOOGLE_API_KEY=your_google_api_key_here
```

**Gemini API 키 발급**: https://makersuite.google.com/app/apikey

#### 3. 챗봇 실행
```bash
python chat_app.py
```

### 사용법
1. 프로그램 실행 시 AI가 먼저 인사말을 합니다
2. 하단 입력창에 질문을 입력하고 Enter 또는 "전송" 버튼 클릭
3. Shift+Enter로 줄바꿈 가능

---

## 📚 RAG Q&A 봇 (FastAPI)

---

## 📚 RAG Q&A 봇 (FastAPI)

### 특징
- 문서 기반 질의응답
- RAG(Retrieval-Augmented Generation) 패턴
- PDF/TXT 문서 학습
- FastAPI REST API

### 실행 방법

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
# .env 파일에 실제 OPENAI_API_KEY 입력 (RAG 봇용)
```

**OpenAI API 키 발급**: https://platform.openai.com/api-keys

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
├── chat_app.py          # GUI 챗봇 (Gemini)
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
