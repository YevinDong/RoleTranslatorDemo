from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict
from typing_extensions import Literal
from dataclasses import dataclass


from langchain.agents import AgentState as BaseAgentState

__all__ = ["GraphState"]

# ----- Graph state -------------------------------------------------------------
RoleLiteral = Literal["product", "developer", "leader", "unknown"]
DirectionLiteral = Literal["product_to_dev", "dev_to_product", "mixed", "none"]


@dataclass
class GraphState:
    # ---- Core turn-level input -------------------------------------------------
    # 当前这一轮的原始用户输入文本，由前端/调用方写入。
    user_input: str

    # ---- Model-inferred role & direction --------------------------------------
    # classify_role 节点推断出的角色：
    # - "product" | "developer" | "leader" | "unknown"
    # - None 表示尚未推断。
    role_inferred: Optional[RoleLiteral] = None

    # classify_role 节点给出的角色置信度 [0.0, 1.0]；
    # None 表示尚未推断或无效。
    role_confidence: Optional[float] = None

    # ---- User override from UI -------------------------------------------------
    # 用户在 UI 中显式声明的角色覆盖：
    # - "product" | "developer" | "leader"
    # - None 表示用户未强制指定，使用模型推断结果。
    role_override_by_user: Optional[RoleLiteral] = None

    # transction_content
    # 理解用户的意图，通过历史信息、上下文、历史信息，生成一个transaction_content，用于最终的翻译
    transction_content: Optional[str] = ""

    # reason
    # ai 判定用户角色的理由
    reason: Optional[str] = ""

    # 运行结果
    result: Optional[str] = ""

    def clone(self, merged: Optional[Dict[str, Any]] = None) -> "GraphState":
        """
        Create a new GraphState with current fields overridden by `merged`.

        Using an intermediate dict avoids
        `TypeError: GraphState() got multiple values for keyword argument`
        when the same key appears in both the current state and `merged`.
        """
        base: Dict[str, Any] = dict(self.__dict__)
        if merged:
            base.update(merged)
        return GraphState(**base)


class GraphContext(TypedDict):
    """Context parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    thread_id: Optional[str] = None
    enable_websearch: bool = False
    enable_thinking: bool = False
