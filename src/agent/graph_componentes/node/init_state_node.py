from agent.state import GraphState


def init_state_node(state: GraphState) -> GraphState:
    """Initialize OR Reset the state."""
    return state.clone({
        "result": None,
        "role_inferred": None,
        "role_confidence": None,
        "reason": None,
        "transction_content": None
    })
