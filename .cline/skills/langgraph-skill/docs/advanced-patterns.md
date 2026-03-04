# LangGraph 고급 패턴

## 멀티에이전트 시스템

### Supervisor 패턴

```python
from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langgraph.types import Command

model = init_chat_model("gpt-4o")

# 서브에이전트 정의
def research_agent(state: MessagesState):
    """검색 전문 에이전트"""
    response = model.invoke([
        {"role": "system", "content": "You are a research specialist."},
        *state["messages"]
    ])
    return {"messages": [response]}

def writer_agent(state: MessagesState):
    """문서 작성 전문 에이전트"""
    response = model.invoke([
        {"role": "system", "content": "You are a technical writer."},
        *state["messages"]
    ])
    return {"messages": [response]}

def supervisor(state: MessagesState) -> Command:
    """어느 에이전트로 라우팅할지 결정"""
    response = model.invoke(state["messages"])
    # 응답 분석 후 다음 에이전트 결정
    if "research" in response.content.lower():
        return Command(goto="research_agent")
    elif "write" in response.content.lower():
        return Command(goto="writer_agent")
    else:
        return Command(goto="__end__")

# 그래프 구성
workflow = StateGraph(MessagesState)
workflow.add_node("supervisor", supervisor)
workflow.add_node("research_agent", research_agent)
workflow.add_node("writer_agent", writer_agent)

workflow.add_edge(START, "supervisor")
workflow.add_edge("research_agent", "supervisor")
workflow.add_edge("writer_agent", "supervisor")

graph = workflow.compile()
```

### 에이전트 핸드오프 (Handoff)

```python
from langgraph.types import Command

def agent_a(state):
    # 작업 완료 후 agent_b로 핸드오프
    return Command(
        goto="agent_b",
        update={"handoff_data": "processed by A"}
    )

def agent_b(state):
    data = state.get("handoff_data")
    # agent_a의 결과를 이어서 처리
    return {"result": f"B processed: {data}"}
```

## RAG (Retrieval-Augmented Generation)

```python
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# 벡터 스토어 설정
embeddings = OpenAIEmbeddings()
docs = [Document(page_content="LangGraph는 AI 에이전트 프레임워크다.")]
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()

# RAG 노드
def retrieve(state):
    question = state["messages"][-1].content
    docs = retriever.invoke(question)
    return {"context": [d.page_content for d in docs]}

def generate(state):
    context = "\n".join(state["context"])
    response = model.invoke([
        {"role": "system", "content": f"Context: {context}"},
        *state["messages"]
    ])
    return {"messages": [response]}

class RAGState(TypedDict):
    messages: Annotated[list, add]
    context: list[str]

workflow = StateGraph(RAGState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)
```

## Middleware (모델 훅)

```python
# before_model: 요청 전 처리
def add_system_prompt(state, config):
    """동적으로 시스템 프롬프트 추가"""
    user_lang = config.get("configurable", {}).get("language", "ko")
    messages = state["messages"]
    system_msg = {"role": "system", "content": f"Respond in {user_lang}"}
    return [system_msg] + messages

# after_model: 응답 후 처리
def log_response(state, response, config):
    """응답 로깅 미들웨어"""
    print(f"Tokens used: {response.usage_metadata}")
    return response

# 모델에 훅 적용
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o").with_config(
    callbacks=[],  # LangSmith 트레이싱
)
```

## MCP (Model Context Protocol)

```python
# FastMCP 서버 구현
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-tools-server")

@mcp.tool()
def get_weather(city: str) -> str:
    """도시의 날씨를 반환한다."""
    return f"{city}: 맑음, 22°C"

@mcp.resource("data://knowledge-base")
def get_knowledge():
    """지식베이스 리소스"""
    return "Company knowledge base content"

# MCP 실행
if __name__ == "__main__":
    mcp.run(transport="stdio")  # stdio or sse

# LangGraph에서 MCP 도구 사용
from langchain_mcp_adapters.client import MultiServerMCPClient

async with MultiServerMCPClient({
    "weather": {
        "command": "python",
        "args": ["weather_server.py"],
        "transport": "stdio"
    }
}) as client:
    tools = client.get_tools()
    agent = create_react_agent(model, tools)
```

## Guardrails (안전 필터)

```python
import re

def pii_guard(state: MessagesState):
    """PII(개인정보) 감지 및 마스킹"""
    messages = state["messages"]

    # 이메일, 전화번호 패턴 감지
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{4}[-.]?\d{4}\b'

    cleaned_messages = []
    for msg in messages:
        if hasattr(msg, 'content'):
            content = msg.content
            content = re.sub(email_pattern, '[EMAIL REDACTED]', content)
            content = re.sub(phone_pattern, '[PHONE REDACTED]', content)
            msg = msg.model_copy(update={"content": content})
        cleaned_messages.append(msg)

    return {"messages": cleaned_messages}

# 그래프에 가드레일 추가
workflow.add_node("pii_guard", pii_guard)
workflow.add_edge(START, "pii_guard")
workflow.add_edge("pii_guard", "call_model")
```

## 스트리밍 - 고급

```python
# 커스텀 이벤트 스트리밍
from langgraph.config import get_stream_writer

async def long_process_node(state):
    writer = get_stream_writer()

    for i in range(10):
        writer({"step": i, "progress": f"{i*10}%"})
        await asyncio.sleep(0.1)

    return {"result": "completed"}

# 비동기 스트리밍 소비
async for chunk in graph.astream(input, config, stream_mode="custom"):
    print(chunk)

# 여러 stream_mode 동시 사용
async for chunk in graph.astream(
    input, config,
    stream_mode=["values", "messages"]
):
    mode, data = chunk
    if mode == "messages":
        token, metadata = data
        print(token.content, end="", flush=True)
```

## 상태 스냅샷 및 되돌리기

```python
# 상태 히스토리 조회
history = list(graph.get_state_history(config))
for state in history:
    print(state.config, state.values)

# 특정 체크포인트로 되돌리기
target_config = history[2].config  # 3번째 스냅샷
graph.invoke(None, target_config)   # 해당 시점부터 재실행
```
