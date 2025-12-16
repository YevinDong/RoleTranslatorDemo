import json
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt.chat_agent_executor import Runtime
import time
from agent.modal import RoleClassifierOutput
from agent.prompt import ROLE_CLASSIFIER_SYSTEM_PROMPT
from agent.state import GraphContext, GraphState
from agent.utils.llm_utils import create_openai_llm
from agent.utils.sqlite_utils import sql_manager


def role_classifier_agent_node(state: GraphState, runtime: Runtime[GraphContext]) -> GraphState:
    """
        role_classifier_agent_node节点，用来区分用户角色，和输入摘要
        通过本地化存储(local sqlite)，通过`摘要记录(历史解析结果)`的方式来保存记忆
        摘要记录方式虽然会丢失语境和稍有偏差，但是对于专业向的agent，这个偏差是可以接受的。
        通过thread_id进行数据隔离
    """
    thread_id = runtime.context["thread_id"]
    llm = create_openai_llm().with_structured_output(RoleClassifierOutput)
    history = []
    sql_record = sql_manager.get_role_classifier_history(thread_id)
    for record in sql_record:
        history.append(record['json'])

    json_input = json.dumps({
        "current_input": state.user_input,
        "role_override_by_user": state.role_override_by_user,
        "conversation_history": history
    }, ensure_ascii=False, indent=2)
    print("role_classifier_agent_node json_input", json_input)

    resp: RoleClassifierOutput = llm.invoke(
        input=[
            SystemMessage(ROLE_CLASSIFIER_SYSTEM_PROMPT),
            HumanMessage(json_input),
        ],
    )

    sql_manager.inset_role_classifier_history(thread_id, json.dumps(
        {
            "user_input": state.user_input,
            "role_inferred": resp.role_inferred,
            "reason": resp.reason,
            "role_confidence": resp.role_confidence,
            "time": int(time.time()*1000)
        },
        ensure_ascii=False
    ))

    return state.clone({
        "role_confidence": resp.role_confidence,
        "role_inferred": resp.role_inferred,
        "reason": resp.reason,
        "transction_content": resp.transction_content
    })
