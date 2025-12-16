from pydantic import BaseModel, Field


class Req(BaseModel):
    user_input: str = Field(..., description="用户问题，必填")
    thread_id: str = Field(..., description="会话id，必填")


class Resp(BaseModel):
    reply: str
