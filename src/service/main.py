import json
from fastapi import FastAPI, Query
from agent.graph import graph as workflow
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.modal import FinallyOutput


class Req(BaseModel):
    user_input: str
    thread_id: str


class Resp(BaseModel):
    reply: FinallyOutput


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/chat", response_model=Resp)
def chat_endpoint(
    user_input: str = Query(..., description="用户输入"),
    thread_id: str = Query(..., description="会话id")
):
    config = {
        "configurable": {
            "thread_id": thread_id,
            "enable_websearch": False,
            "enable_thinking": False
        }
    }
    state_input = {"user_input": user_input}
    resp = workflow.invoke(state_input, config)
    return Resp(reply=resp)


@app.get("/stream")
async def chat_endpoint(
    user_input: str = Query(..., description="用户输入"),
    thread_id: str = Query(..., description="会话id")
):
    config = {
        "configurable": {
            "thread_id": thread_id,
            "enable_websearch": False,
            "enable_thinking": False
        }
    }
    state_input = {"user_input": user_input}
    # TODO sse应该是订阅机制，但是这里就是模拟一下直接触发workflow了
    # 前端根据thread_id订阅sse，然后前端post数据给后台，后台接到后给前端sse推送
    # 目前这个设计有点畸形了
    # TODO stream 这里直接把所有snapshot状态暴漏了，其实不符合规范

    async def sse_generator():
        async for chunk in workflow.astream(state_input, config):
            node_name, snapshot = next(iter(chunk.items()))
            data = json.dumps({
                "node_name": node_name,
                "snapshot": snapshot
            })
            yield f"event: send\ndata: {data}\n\n"

        # 发送结束事件
        yield f"event: end\ndata: Stream finished\n\n"

    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )
