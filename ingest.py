"""
문서 임베딩 및 벡터 DB 저장 스크립트
사용법: python ingest.py
"""
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 환경 변수 로드
load_dotenv()

# 상수 정의
PDF_PATH = "document.pdf"  # 여기에 실제 PDF 파일 경로를 지정하세요
DB_PATH = "./db"  # 벡터 DB 저장 경로
CHUNK_SIZE = 1000  # 문서 분할 크기
CHUNK_OVERLAP = 200  # 청크 간 겹침


def main():
    """문서를 로드하고 벡터 DB에 저장하는 메인 함수"""
    
    print("🔄 Step 1: PDF 문서 로드 중...")
    # PyPDFLoader로 PDF 파일 로드
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"❌ PDF 파일을 찾을 수 없습니다: {PDF_PATH}")
    
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    print(f"✅ {len(documents)} 페이지 로드 완료")
    
    print("\n🔄 Step 2: 문서 분할 중...")
    # RecursiveCharacterTextSplitter로 문서 분할
    # 이 도구는 의미 단위로 문서를 나누어 검색 성능을 높입니다
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    splits = text_splitter.split_documents(documents)
    print(f"✅ {len(splits)}개의 청크로 분할 완료")
    
    print("\n🔄 Step 3: 임베딩 생성 및 벡터 DB 저장 중...")
    # OpenAI 임베딩 모델 초기화
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002"  # OpenAI의 임베딩 모델
    )
    
    # ChromaDB에 문서 저장
    # persist_directory: 디스크에 영구 저장할 경로
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    print(f"✅ 벡터 DB 저장 완료: {DB_PATH}")
    print(f"\n📊 요약:")
    print(f"  - 원본 페이지: {len(documents)}")
    print(f"  - 분할된 청크: {len(splits)}")
    print(f"  - 저장 위치: {DB_PATH}")
    print("\n✨ 데이터 준비가 완료되었습니다!")


if __name__ == "__main__":
    main()
