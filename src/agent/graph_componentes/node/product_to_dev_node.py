from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt.chat_agent_executor import Runtime
from agent.prompt import PRODUCT_TO_DEV_SYSTEM_PROMPT
from agent.state import GraphState
from agent.utils.llm_utils import create_openai_llm


def product_to_dev_node(state: GraphState) -> GraphState:
    """
    product_to_dev_node节点，用来输出在产品->dev的翻译。
    不需要存储上下文。每一次解析都是通过整理好的数据重新生成翻译结果。
    """
    llm = create_openai_llm()
    resp = llm.invoke(
        input=[
            SystemMessage(PRODUCT_TO_DEV_SYSTEM_PROMPT),
            HumanMessage(state.transction_content),
        ],
    )

    return state.clone({
        "result": resp.content
    })
