import json
from fastapi import FastAPI
from .model import Req, Resp
from agent.graph import graph as workflow

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=Resp)
def chat_endpoint(req: Req):
    config = {
        "configurable": {
            "thread_id": req.thread_id,
            "enable_websearch": False,
            "enable_thinking": False
        }
    }
    state_input = {"user_input": req.user_input}
    resp = workflow.invoke(state_input, config)
    print(resp)
    return Resp(reply=resp)
