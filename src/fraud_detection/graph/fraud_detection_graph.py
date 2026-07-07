from langgraph.graph import StateGraph, START, END
from src.fraud_detection.state.state import AgentState
from src.fraud_detection.nodes.registrar_scout_node import registrar_scout_node
from src.fraud_detection.nodes.geospatial_analyst_node import geospatial_analyst_node
from src.fraud_detection.nodes.digital_footprint_node import digital_footprint_node
from src.fraud_detection.nodes.supervisor_node import supervisor_node
from src.fraud_detection.nodes.human_analyst_node import human_analyst_node
from src.fraud_detection.state.state import AgentState


def human_analyst_node_router(state:AgentState):
    """
    Reads the supervisor's final decision and routes the graph dynamically.
    """

    investigation_status = state.get("investigation_status")

    if investigation_status == "cleared":
        return "end_investigation"
    else:
        # If pending or escalated, send it to the human!
        return "route_to_human" 



workflow = StateGraph(AgentState)

## Adding the Nodes

workflow.add_node("registrar_scout_node" , registrar_scout_node)
workflow.add_node("geospatial_analyst_node" , geospatial_analyst_node)
workflow.add_node("digital_footprint_node" , digital_footprint_node)
workflow.add_node("supervisor_node" , supervisor_node)
workflow.add_node("human_analyst_node" , human_analyst_node)

## Adding Edges
workflow.add_edge(START , "registrar_scout_node")
workflow.add_edge("registrar_scout_node" , "geospatial_analyst_node")
workflow.add_edge("registrar_scout_node" , "digital_footprint_node")


workflow.add_edge("geospatial_analyst_node" , "supervisor_node")
workflow.add_edge("digital_footprint_node" , "supervisor_node")

workflow.add_conditional_edges(
    "supervisor_node",
    human_analyst_node_router,
    {
        "route_to_human" : "human_analyst_node",
        "end_investigation" : END
    }
)
workflow.add_edge("human_analyst_node" , END)



graph_builder = workflow.compile()