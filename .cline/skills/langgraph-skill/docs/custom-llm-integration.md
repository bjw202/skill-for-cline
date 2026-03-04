# 사내 Custom LLM API 연동 상세 가이드

LangChain/LangGraph에서 사내 내부 LLM API를 사용하는 방법.

---

## 배경: 사내 API 엔드포인트 구조

회사 내부 LLM 게이트웨이는 보통 다음 두 가지 형식 중 하나를 따른다:

| 형식 | 요청 경로 | 인증 헤더 | 응답 구조 |
|------|----------|----------|---------|
| OpenAI 호환 | `POST /v1/chat/completions` | `Authorization: Bearer <key>` | `choices[0].message.content` |
| Anthropic 호환 | `POST /v1/messages` | `x-api-key: <key>` | `content[0].text` |

**예시 사내 경로** `POST /openapi/chat/v1/messages`:
- `/v1/messages` 접미사 → Anthropic 형식 가능성 높음
- `/openapi/chat` 프리픽스는 사내 게이트웨이 라우팅

**형식 확인 방법:** API 담당자에게 요청 바디/응답 구조를 확인하거나 curl로 테스트.

```bash
# Anthropic 형식 테스트
curl -X POST https://사내도메인/openapi/chat/v1/messages \
  -H "x-api-key: your-key" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"model":"모델명","max_tokens":100,"messages":[{"role":"user","content":"hello"}]}'
```

---

## 방법 1: ChatAnthropic (Anthropic 호환 엔드포인트)

### 설치

```bash
pip install langchain-anthropic
```

### 기본 사용

```python
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatAnthropic(
    model="사내-모델명",
    base_url="https://사내도메인",
    # SDK 내부에서 base_url + /v1/messages 로 요청
    anthropic_api_key="내부-api-key",
    max_tokens=1024,
    temperature=0.7,
    default_headers={
        "X-Internal-Token": "게이트웨이-추가헤더",
    },
)

response = llm.invoke([
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="안녕하세요"),
])
print(response.content)
```

### 환경 변수 방식

```bash
export ANTHROPIC_BASE_URL="https://사내도메인"
export ANTHROPIC_API_KEY="내부-api-key"
```

```python
llm = ChatAnthropic(model="사내-모델명")  # 환경 변수 자동 사용
```

### LangGraph에서 사용

```python
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.memory import InMemorySaver

def call_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")
graph = builder.compile(checkpointer=InMemorySaver())
```

---

## 방법 2: ChatOpenAI (OpenAI 호환 엔드포인트)

### 설치

```bash
pip install langchain-openai
```

### 기본 사용

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="사내-모델명",
    base_url="https://사내도메인/openapi/chat/v1",
    # SDK 내부에서 base_url + /chat/completions 로 요청
    api_key="내부-api-key",
    temperature=0.7,
    max_tokens=1024,
    default_headers={
        "X-Internal-Token": "게이트웨이-추가헤더",
    },
    extra_body={
        "custom_param": "value",  # 비표준 파라미터 전달
    },
)
```

**주의:** `ChatOpenAI`는 `base_url`에 `/chat/completions`를 자동 추가한다.
엔드포인트가 `https://host/openapi/chat/v1/messages`라면:
- `base_url = "https://host/openapi/chat/v1"` (suffix 제거)
- SDK가 `/chat/completions`를 붙이므로 경로 불일치 발생
- 이 경우 방법 3(Custom BaseChatModel)을 사용한다.

---

## 방법 3: Custom BaseChatModel (완전 제어)

SDK가 경로를 자동 추가해서 충돌하거나, 인증 방식이 비표준일 때 사용.

### 동기 + 비동기 완전 구현

```python
import asyncio
import requests
import httpx
from typing import Any, Dict, List, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
    AsyncCallbackManagerForLLMRun,
)
from pydantic import Field, SecretStr


class InternalLLMChat(BaseChatModel):
    """사내 LLM API를 LangChain BaseChatModel로 래핑"""

    endpoint_url: str = Field(description="전체 엔드포인트 URL")
    api_key: SecretStr = Field(description="내부 API 키")
    model_name: str = Field(default="default-model")
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=1024)
    timeout: int = Field(default=30)
    max_retries: int = Field(default=3)
    api_format: str = Field(default="anthropic",
                            description="'anthropic' 또는 'openai'")
    extra_headers: Dict[str, str] = Field(default_factory=dict)

    @property
    def _llm_type(self) -> str:
        return "internal-llm"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {"model": self.model_name, "api_format": self.api_format}

    def _build_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_format == "anthropic":
            headers["x-api-key"] = self.api_key.get_secret_value()
            headers["anthropic-version"] = "2023-06-01"
        else:
            headers["Authorization"] = f"Bearer {self.api_key.get_secret_value()}"
        headers.update(self.extra_headers)
        return headers

    def _build_payload(self, messages: List[BaseMessage]) -> Dict[str, Any]:
        system = ""
        chat_msgs = []
        for m in messages:
            if isinstance(m, SystemMessage):
                system = m.content
            elif isinstance(m, HumanMessage):
                chat_msgs.append({"role": "user", "content": m.content})
            else:
                chat_msgs.append({"role": "assistant", "content": m.content})

        if self.api_format == "anthropic":
            payload: Dict[str, Any] = {
                "model": self.model_name,
                "max_tokens": self.max_tokens,
                "messages": chat_msgs,
                "temperature": self.temperature,
            }
            if system:
                payload["system"] = system
        else:
            all_msgs = []
            if system:
                all_msgs.append({"role": "system", "content": system})
            all_msgs.extend(chat_msgs)
            payload = {
                "model": self.model_name,
                "messages": all_msgs,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }
        return payload

    def _parse_response(self, data: Dict[str, Any]) -> str:
        if self.api_format == "anthropic":
            return data["content"][0]["text"]
        return data["choices"][0]["message"]["content"]

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        headers = self._build_headers()
        payload = self._build_payload(messages)
        if stop:
            payload["stop_sequences" if self.api_format == "anthropic" else "stop"] = stop

        for attempt in range(self.max_retries):
            try:
                resp = requests.post(
                    self.endpoint_url, json=payload,
                    headers=headers, timeout=self.timeout,
                )
                resp.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                if attempt + 1 == self.max_retries:
                    raise RuntimeError(f"API 호출 실패: {e}") from e

        text = self._parse_response(resp.json())
        return ChatResult(generations=[
            ChatGeneration(message=AIMessage(content=text), generation_info=resp.json())
        ])

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        headers = self._build_headers()
        payload = self._build_payload(messages)
        if stop:
            payload["stop_sequences" if self.api_format == "anthropic" else "stop"] = stop

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for attempt in range(self.max_retries):
                try:
                    resp = await client.post(
                        self.endpoint_url, json=payload, headers=headers
                    )
                    resp.raise_for_status()
                    break
                except httpx.HTTPError as e:
                    if attempt + 1 == self.max_retries:
                        raise RuntimeError(f"API 호출 실패: {e}") from e
                    await asyncio.sleep(2 ** attempt)

        text = self._parse_response(resp.json())
        return ChatResult(generations=[
            ChatGeneration(message=AIMessage(content=text))
        ])
```

### 사용 예시

```python
# 직접 호출
llm = InternalLLMChat(
    endpoint_url="https://사내도메인/openapi/chat/v1/messages",
    api_key="내부-api-key",
    model_name="사내-모델명",
    api_format="anthropic",
    extra_headers={"X-Corp-Client": "my-service"},
)

# LangChain 체인에서
from langchain_core.prompts import ChatPromptTemplate

chain = ChatPromptTemplate.from_messages([
    ("system", "{domain} 전문가입니다."),
    ("human", "{question}")
]) | llm

result = chain.invoke({"domain": "재무", "question": "ROI란 무엇인가요?"})

# LangGraph 노드에서
def call_internal_model(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

---

## 방법 선택 가이드

```
엔드포인트 경로 확인
        │
        ├─ /v1/messages 포함
        │         └─→ ChatAnthropic + base_url (방법 1) 먼저 시도
        │
        ├─ /v1/chat/completions 포함
        │         └─→ ChatOpenAI + base_url (방법 2)
        │
        └─ 경로 고정 or SDK 경로 충돌 or 비표준 인증
                  └─→ Custom BaseChatModel (방법 3)
```

| 조건 | 권장 방법 |
|------|----------|
| `/v1/messages` 경로 | 방법 1 (ChatAnthropic) |
| OpenAI 호환 확인됨 | 방법 2 (ChatOpenAI) |
| SDK 경로 자동 추가 충돌 | 방법 3 |
| JWT/사내 SSO 인증 | 방법 3 (`extra_headers`로 처리) |
| 비동기 성능 필요 | 방법 3 (`_agenerate` 구현) |

---

## 트러블슈팅

| 증상 | 원인 | 해결 |
|------|------|------|
| `404 Not Found` | SDK가 경로 자동 추가로 경로 불일치 | `base_url` 조정 or 방법 3 사용 |
| `401 Unauthorized` | 인증 헤더 형식 불일치 | `extra_headers`로 수동 지정 |
| `422 Unprocessable` | 요청 바디 형식 불일치 | Anthropic vs OpenAI 형식 전환 |
| 응답 파싱 에러 | API 형식 오판 | 실제 응답 구조 출력 후 `api_format` 조정 |
| 타임아웃 | DRM/게이트웨이 지연 | `timeout` 값 늘리기 (60 이상) |
