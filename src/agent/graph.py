"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from langgraph.graph import StateGraph, START, END

import agent.graph_componentes as gc
from agent.state import GraphContext, GraphState
from agent.utils.sqlite_utils import SqlManager


def create_graph() -> StateGraph:
    """Create a graph."""

    # init graph
    graph = StateGraph(GraphState, context_schema=GraphContext)

    # add nodes
    graph.add_node("role_classifier_agent_node",
                   gc.node.role_classifier_agent_node)
    graph.add_node("init_state_node", gc.node.init_state_node)
    graph.add_node("end_generate_msg_node", gc.node.end_generate_msg_node)
    graph.add_node("product_to_dev_node", gc.node.product_to_dev_node)
    graph.add_node("dev_to_product_node", gc.node.dev_to_product_node)
    graph.add_node("archiver_node", gc.node.archiver_node)
    graph.add_node("output_node", gc.node.output_node)

    # add edges
    graph.add_edge(START, "init_state_node")
    graph.add_edge("init_state_node", "role_classifier_agent_node")
    graph.add_edge("product_to_dev_node", "archiver_node")
    graph.add_edge("dev_to_product_node", "archiver_node")
    graph.add_edge("end_generate_msg_node", "output_node")
    graph.add_edge("archiver_node", "output_node")
    graph.add_edge("output_node", END)

    # add conditional edges (LangGraph >= 1.0 API)
    graph.add_conditional_edges(
        "role_classifier_agent_node",
        gc.conditional.route_by_role_conditional,
        {
            "end_generate_msg_node": "end_generate_msg_node",
            "dev_to_product_node": "dev_to_product_node",
            "product_to_dev_node": "product_to_dev_node",
        },
    )

    return graph.compile()


# Define the graph
graph = create_graph()
