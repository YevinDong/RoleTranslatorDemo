
from typing import Optional
from pydantic import BaseModel, Field

from agent.state import DirectionLiteral, RoleLiteral


class RoleClassifierOutput(BaseModel):
    role_inferred: Optional[RoleLiteral] = Field(
        ..., description="inferred role")
    role_confidence: Optional[float] = Field(...,
                                             description="role confidence")
    reason: str = Field(..., description="reasons for decision")
    current_input: str = Field(..., description="current sesstion user input")
    transction_content: str = Field(...,
                                    description="Integrate transction content raised by users")


class FinallyOutput(BaseModel):
    """Final output of the role routing agent."""
    role_inferred: Optional[RoleLiteral] = Field(
        ..., description="inferred role")
    role_confidence: Optional[float] = Field(...,
                                             description="role confidence")
    transction_content: str = Field(...,
                                    description="Integrate transction content raised by users")
    result: str = Field(..., description="result")
    reson: str = Field(..., description="reson")
