from langgraph.prebuilt.chat_agent_executor import Runtime
from agent.state import GraphContext, GraphState


def archiver_node(state: GraphState, runtime: Runtime[GraphContext]) -> GraphState:
    """
        archiver_node节点，用于归纳总结传递过来的信息。
        如果增加leader角色需要在这里将dev和product角色的输出进行整合
        目前还不需要二次整理，其实可以通过更好的模型进行二次拓展
    """
    return state.clone({
        "result": state.result
    })
