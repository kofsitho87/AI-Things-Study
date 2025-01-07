# LangChain & Llama-index 튜토리얼

이 프로젝트는 LangChain과 Llama-index를 활용한 RAG(Retrieval Augmented Generation) 시스템과 AI Agent 개발을 위한 튜토리얼 모음입니다.

## 소개

RAG 시스템에서는 기존의 키워드 기반 검색 방식의 한계를 극복하기 위해 LLM과 벡터 임베딩 기술을 활용합니다:
- **LLM (Large Language Model)**: 텍스트 데이터의 패턴을 깊이 이해하여 사용자 질문에 관련된 답변을 생성
- **벡터 임베딩**: 단어, 문장, 또는 문서의 의미를 벡터 형태로 표현하여 문서 간 유사도를 빠르게 계산

## 프로젝트 구조

### Llama-index
- **VectorStore**: Vector Database 활용 가이드
  - Vector DB 기본 개념 및 특징
  - Simple Vector Store 구현
  - Chroma DB 활용 방법
  - RAG 시스템에서의 Vector Database 역할

## Vector Database 소개

Vector Database는 RAG 시스템에서 중요한 역할을 하며 다음과 같은 특징이 있습니다:

1. **데이터 표현**
   - 전통적인 데이터베이스: 테이블, 행, 열 형태로 데이터 저장
   - 벡터 데이터베이스: 벡터(고차원 수학적 표현) 형태로 데이터 저장

2. **쿼리 방식**
   - 전통적인 데이터베이스: 키나 특정 속성값 기반의 정확한 매칭
   - 벡터 데이터베이스: 유사도 기반 쿼리 사용

3. **최적화 기술**
   - ANN(Approximate Nearest Neighbor) 검색
   - 해싱, 양자화, 그래프 기반 검색 등의 기술 활용

## 시작하기

### 필수 라이브러리 설치

```bash
pip install llama-index-vector-stores-qdrant qdrant_client
```

### 예제 실행
프로젝트에는 TechCrunch 기사를 활용한 실제 구현 예제가 포함되어 있습니다.
