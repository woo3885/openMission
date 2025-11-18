"""
FastAPI + LangChain RAG Q&A Bot
2주 해커톤 프로젝트
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# 환경 변수 로드
load_dotenv()

# OpenAI API 키 확인
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY가 .env 파일에 설정되지 않았습니다!")

# FastAPI 앱 생성
app = FastAPI(
    title="RAG Q&A Bot API",
    description="LangChain을 사용한 문서 기반 Q&A 시스템",
    version="0.1.0"
)

# 벡터 DB 경로
DB_PATH = "./db"

# 1️⃣ Retriever 생성 (검색기)
# 디스크에 저장된 벡터 DB를 불러와서 검색 가능한 상태로 만듭니다
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = Chroma(
    persist_directory=DB_PATH,
    embedding_function=embeddings
)
# retriever는 질문과 유사한 문서 청크를 찾아옵니다
retriever = vectorstore.as_retriever(
    search_type="similarity",  # 유사도 기반 검색
    search_kwargs={"k": 3}  # 상위 3개 결과만 가져오기
)

# 2️⃣ Prompt Template 정의
# 검색된 문맥(context)과 사용자 질문(question)을 LLM에 전달하는 형식을 정의합니다
template = """당신은 제공된 문서를 기반으로 질문에 답변하는 AI 어시스턴트입니다.
아래의 문맥(context)을 참고하여 질문에 답변해주세요.
만약 문맥에서 답을 찾을 수 없다면, "제공된 문서에서 관련 정보를 찾을 수 없습니다"라고 답변하세요.

문맥:
{context}

질문: {question}

답변:"""

prompt = ChatPromptTemplate.from_template(template)

# 3️⃣ LLM 정의
# GPT-4o 모델을 사용합니다
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0  # 일관된 답변을 위해 temperature를 0으로 설정
)

# 4️⃣ RAG 체인 구성 (LCEL 사용)
# LCEL(LangChain Expression Language)로 파이프라인을 연결합니다
# 흐름: 질문 → Retriever(검색) → Prompt → LLM → OutputParser(결과 정리)

def format_docs(docs):
    """검색된 문서를 하나의 문자열로 결합"""
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {
        "context": retriever | format_docs,  # retriever로 문서 검색 후 포맷팅
        "question": RunnablePassthrough()  # 질문을 그대로 전달
    }
    | prompt  # 프롬프트 템플릿 적용
    | llm  # LLM으로 답변 생성
    | StrOutputParser()  # 결과를 문자열로 파싱
)


@app.get("/")
async def root():
    """서버 상태 확인"""
    return {
        "message": "Hello World",
        "status": "running",
        "project": "LangChain RAG Q&A Bot",
        "rag_chain_ready": True
    }


# 📌 요청/응답 모델 정의
class QuestionRequest(BaseModel):
    """질문 요청 모델"""
    question: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "문서의 주요 내용은 무엇인가요?"
            }
        }


class AnswerResponse(BaseModel):
    """답변 응답 모델"""
    question: str
    answer: str


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    문서 기반 질문에 답변하는 엔드포인트
    
    - **question**: 사용자의 질문
    
    Returns:
    - **question**: 입력받은 질문
    - **answer**: RAG 체인이 생성한 답변
    """
    try:
        # RAG 체인 실행
        # invoke()는 동기 함수지만, FastAPI는 자동으로 비동기 처리합니다
        answer = rag_chain.invoke(request.question)
        
        return AnswerResponse(
            question=request.question,
            answer=answer
        )
    
    except Exception as e:
        # 오류 발생 시 상세 정보 반환
        raise HTTPException(
            status_code=500,
            detail=f"답변 생성 중 오류가 발생했습니다: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
