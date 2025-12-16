
from agent.modal import FinallyOutput
from agent.state import GraphState


def output_node(state: GraphState) -> GraphState:
    """
        output_node 用于最终输出的节点，流程结束的时候过滤信息，将没必要暴漏的信息进行隐藏。
        同时作为结束节点，做一些全局state的清理工作。
    """

    return FinallyOutput(
        result=state.result,
        role_confidence=state.role_confidence,
        role_inferred=state.role_inferred,
        transction_content=state.transction_content,
        reson=state.reason
    )
