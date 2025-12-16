from langgraph.prebuilt.chat_agent_executor import Runtime
from agent.prompt import gen_end_generate_msg_prompt
from agent.state import GraphState
from agent.utils.llm_utils import create_openai_llm


def end_generate_msg_node(state: GraphState) -> GraphState:
    """
    end_generate_msg_node节点，用于生成结束生成消息。
    在role_classifier_agent_node判断不明的时候生成一些引导话术。
    """
    llm = create_openai_llm()
    resp = llm.invoke(gen_end_generate_msg_prompt(state))

    return state.clone({
        "result": resp.content
    })
