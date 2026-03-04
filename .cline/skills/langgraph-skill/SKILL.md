---
name: langgraph-skill
description: |
  LangGraph를 사용한 AI 에이전트 워크플로우를 설계하고 구현한다. StateGraph, 노드/엣지 구성,
  메모리(Checkpointer), 스트리밍, Human-in-the-Loop, 멀티에이전트 패턴을 다룬다.
  사내 Custom LLM API(OpenAI/Anthropic 호환 엔드포인트)를 LangChain/LangGraph에 연동하는 방법도 포함한다.
  Activate on: LangGraph, 랭그래프, StateGraph, 에이전트 그래프, agent workflow,
  langgraph 에이전트, 멀티에이전트, multi-agent, checkpointer, human-in-the-loop,
  스트리밍 에이전트, langgraph 설치, langgraph 튜토리얼, langgraph 메모리, langgraph streaming,
  사내 LLM, custom LLM, 사내 API 연동, OpenAI 호환, Anthropic 호환, BaseChatModel,
  내부 LLM 연동, internal LLM, custom endpoint, ChatOpenAI base_url, ChatAnthropic base_url
---

# LangGraph 에이전트 워크플로우

LangGraph는 상태 기반 AI 에이전트를 그래프로 모델링하는 저수준 오케스트레이션 프레임워크다.
노드(Node)가 작업을 수행하고, 엣지(Edge)가 다음 노드를 결정한다.

## 설치 및 설정

```bash
pip install langgraph langchain-openai langchain-anthropic
```

`.env` 파일:
```
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

UV 사용 시:
```bash
uv add langgraph langchain-openai langchain-anthropic
```

## 핵심 개념

### 3대 구성요소

| 구성요소 | 역할 | 예시 |
|---------|------|------|
| **State** | 그래프 전체가 공유하는 데이터 구조 | TypedDict, MessagesState |
| **Node** | 상태를 받아 처리 후 업데이트 반환 | def call_model(state) → dict |
| **Edge** | 다음 노드 결정 (조건부 or 고정) | add_edge, add_conditional_edges |

### 최소 StateGraph 패턴

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    messages: Annotated[list, add]

def my_node(state: State):
    # 처리 로직
    return {"messages": ["response"]}

# 그래프 구성
workflow = StateGraph(State)
workflow.add_node("my_node", my_node)
workflow.add_edge(START, "my_node")
workflow.add_edge("my_node", END)

# 컴파일 및 실행
graph = workflow.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "session-1"}}
result = graph.invoke({"messages": ["hello"]}, config)
```

### MessagesState (채팅 에이전트 기본)

```python
from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4o-mini")

def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")
graph = builder.compile(checkpointer=InMemorySaver())
```

## 메모리 / Checkpointer

### 단기 메모리 (세션 내)

```python
from langgraph.checkpoint.memory import InMemorySaver

# 개발/테스트용 - 프로세스 재시작 시 초기화
graph = workflow.compile(checkpointer=InMemorySaver())

# thread_id로 대화 세션 구분
config = {"configurable": {"thread_id": "user-123"}}
graph.invoke(input, config)
```

### 장기 메모리 (영속 저장)

```python
# PostgreSQL (프로덕션 권장)
from langgraph.checkpoint.postgres import PostgresSaver

DB_URI = "postgresql://user:pass@localhost:5432/db"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    graph = workflow.compile(checkpointer=checkpointer)

# MongoDB
from langgraph.checkpoint.mongodb import MongoDBSaver

with MongoDBSaver.from_conn_string("localhost:27017") as checkpointer:
    graph = workflow.compile(checkpointer=checkpointer)
```

### Store (크로스 스레드 장기 메모리)

```python
from langgraph.store.memory import InMemoryStore

store = InMemoryStore()
# namespace로 사용자/컨텍스트 분리
namespace = ("user", "alice", "preferences")
store.put(namespace, "theme", {"value": "dark"})
item = store.get(namespace, "theme")
```

## 스트리밍

```python
# stream_mode 옵션
for chunk in graph.stream(input, config, stream_mode="values"):
    # 각 스텝 후 전체 상태 출력
    print(chunk)

for chunk in graph.stream(input, config, stream_mode="updates"):
    # 각 스텝의 변경분만 출력
    print(chunk)

for chunk in graph.stream(input, config, stream_mode="messages"):
    # 토큰 단위 스트리밍 (LLM 출력)
    print(chunk)

# 커스텀 스트림 (노드 내에서)
from langgraph.config import get_stream_writer

def my_node(state):
    writer = get_stream_writer()
    writer({"progress": "50%"})
    return {"messages": [...]}
```

## Human-in-the-Loop

```python
# 특정 노드 전후에 중단
graph = workflow.compile(
    checkpointer=InMemorySaver(),
    interrupt_before=["approval_node"],  # 노드 실행 전 중단
    # interrupt_after=["risky_node"],    # 노드 실행 후 중단
)

# 실행 → 중단 → 상태 확인
config = {"configurable": {"thread_id": "1"}}
graph.invoke(input, config)  # interrupt_before에서 멈춤

# 현재 상태 확인
state = graph.get_state(config)
print(state.next)  # 다음 실행될 노드

# 상태 수정 후 재개
graph.update_state(config, {"approved": True})
graph.invoke(None, config)  # None으로 재개
```

## 도구(Tools) 연동

```python
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

@tool
def search(query: str) -> str:
    """웹 검색을 수행한다."""
    return f"Results for: {query}"

@tool
def calculator(expr: str) -> float:
    """수식을 계산한다."""
    return eval(expr)

# ReAct 에이전트 (도구 사용 루프 내장)
agent = create_react_agent(
    model=init_chat_model("gpt-4o"),
    tools=[search, calculator],
    checkpointer=InMemorySaver()
)
```

## 조건부 엣지 (라우팅)

```python
from langgraph.graph import END

def should_continue(state: State) -> str:
    """다음 노드를 결정하는 라우터 함수"""
    if state["needs_approval"]:
        return "approval"
    elif state["is_complete"]:
        return END
    else:
        return "process"

workflow.add_conditional_edges(
    "check_status",
    should_continue,
    {
        "approval": "approval_node",
        "process": "process_node",
        END: END
    }
)
```

## 사내 Custom LLM API 연동

사내 LLM 엔드포인트를 LangChain/LangGraph 모델로 래핑하는 3가지 방법.

### 엔드포인트 형식 판별

| 경로 패턴 | 형식 | 사용 클래스 |
|----------|------|-----------|
| `/v1/messages` 포함 | Anthropic | `ChatAnthropic` |
| `/v1/chat/completions` 포함 | OpenAI | `ChatOpenAI` |
| 고정 전체 경로 | 비표준 | `BaseChatModel` 상속 |

**응답 구조로 최종 확인:**
- Anthropic: `{"content": [{"type": "text", "text": "..."}]}`
- OpenAI: `{"choices": [{"message": {"content": "..."}}]}`

### 방법 1: ChatAnthropic (`/v1/messages` 형식)

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="사내-모델명",
    # SDK가 base_url + /v1/messages 로 요청
    base_url="https://사내도메인",
    anthropic_api_key="내부-api-key",
    max_tokens=1024,
    default_headers={"X-Internal-Token": "게이트웨이-헤더"},
)
```

### 방법 2: ChatOpenAI (OpenAI 호환 형식)

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="사내-모델명",
    # SDK가 base_url + /chat/completions 로 요청
    base_url="https://사내도메인/openapi/chat/v1",
    api_key="내부-api-key",
    default_headers={"X-Internal-Token": "게이트웨이-헤더"},
)
```

### 방법 3: Custom BaseChatModel (경로 고정 / 비표준 인증)

```python
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field, SecretStr
import requests

class InternalLLM(BaseChatModel):
    endpoint_url: str           # 전체 URL 직접 지정
    api_key: SecretStr
    model_name: str = "default"
    max_tokens: int = 1024
    api_format: str = "anthropic"  # "anthropic" or "openai"

    @property
    def _llm_type(self) -> str:
        return "internal-llm"

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        headers = {"Content-Type": "application/json"}
        if self.api_format == "anthropic":
            headers["x-api-key"] = self.api_key.get_secret_value()
            headers["anthropic-version"] = "2023-06-01"
        else:
            headers["Authorization"] = f"Bearer {self.api_key.get_secret_value()}"

        system = next((m.content for m in messages
                       if m.__class__.__name__ == "SystemMessage"), "")
        chat_msgs = [
            {"role": "user" if m.__class__.__name__ == "HumanMessage" else "assistant",
             "content": m.content}
            for m in messages if m.__class__.__name__ != "SystemMessage"
        ]
        payload = {"model": self.model_name, "max_tokens": self.max_tokens,
                   "messages": chat_msgs}
        if system and self.api_format == "anthropic":
            payload["system"] = system

        resp = requests.post(self.endpoint_url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        text = (data["content"][0]["text"] if self.api_format == "anthropic"
                else data["choices"][0]["message"]["content"])
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=text))])

# 사용
llm = InternalLLM(
    endpoint_url="https://사내도메인/openapi/chat/v1/messages",
    api_key="내부-api-key",
    api_format="anthropic",
)

# LangGraph 노드에서 그대로 사용
def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

상세 코드 및 비동기 지원 → `docs/custom-llm-integration.md` 참조

---

## 상세 패턴

상세 내용은 `docs/advanced-patterns.md` 참조:
- 멀티에이전트 시스템 (Supervisor 패턴, 에이전트 핸드오프)
- RAG (Retrieval-Augmented Generation) 패턴
- MCP (Model Context Protocol) 연동
- Middleware (before/after 모델 훅)
- Guardrails (PII 보호, 안전 필터)

## 공식 링크

| 리소스 | URL |
|--------|-----|
| 공식 문서 | https://langchain-ai.github.io/langgraph/ |
| API Reference | https://langchain-ai.github.io/langgraph/reference/ |
| 공식 튜토리얼 | https://langchain-ai.github.io/langgraph/tutorials/ |
| How-to Guides | https://langchain-ai.github.io/langgraph/how-tos/ |
| 개념 설명 | https://langchain-ai.github.io/langgraph/concepts/ |
| GitHub | https://github.com/langchain-ai/langgraph |
| Python 통합 가이드 | https://python.langchain.com/docs/langgraph |
| 한국어 튜토리얼 (TeddyNote Lab) | https://github.com/teddynote-lab/langgraph-v1-tutorial |
| LangSmith (모니터링) | https://smith.langchain.com |
| LangGraph Cloud | https://langchain-ai.github.io/langgraph/cloud/ |
