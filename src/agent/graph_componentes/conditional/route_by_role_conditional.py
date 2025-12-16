from typing import Literal
from langgraph.prebuilt.chat_agent_executor import Runtime
from agent.state import GraphContext, GraphState


def route_by_role_conditional(state: GraphState, runtime: Runtime[GraphContext]) -> Literal["end_generate_msg_node", "dev_to_product_node", "product_to_dev_node"]:
    """
    route_by_role_conditional节点，用于分类下一步的逻辑。
    默认情况下，如果role_confidence小于0.5，则结束流程，返回结果。
    如果role_confidence大于0.5，则根据role_inferred的值进行下一步的逻辑。

    当然可以在这里进行人工干涉。或者一些hook。
    """
    if state.role_confidence is None or state.role_confidence < 0.5:
        return "end_generate_msg_node"
    elif not state.transction_content or state.transction_content.startswith("ERR:"):
        return "end_generate_msg_node"
    elif state.role_inferred == "developer":
        return "dev_to_product_node"
    elif state.role_inferred == "product":
        return "product_to_dev_node"
    else:
        return "end_generate_msg_node"
