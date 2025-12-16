from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt.chat_agent_executor import Runtime
from agent.prompt import DEV_TO_PRODUCT_SYSTEM_PROMPT
from agent.state import GraphContext, GraphState
from agent.utils.llm_utils import create_openai_llm


def dev_to_product_node(state: GraphState, runtime: Runtime[GraphContext]) -> GraphState:
    """
    dev_to_product_node节点，用来输出在dev->产品的翻译。
    不需要存储上下文。每一次解析都是通过整理好的数据重新生成翻译结果。
    """
    llm = create_openai_llm()
    resp = llm.invoke(
        input=[
            SystemMessage(DEV_TO_PRODUCT_SYSTEM_PROMPT),
            HumanMessage(state.transction_content),
        ],
    )

    return state.clone({
        "result": resp.content
    })
