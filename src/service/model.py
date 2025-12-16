from pydantic import BaseModel

from agent.modal import FinallyOutput


class Req(BaseModel):
    user_input: str
    thread_id: str


class Resp(BaseModel):
    reply: FinallyOutput
