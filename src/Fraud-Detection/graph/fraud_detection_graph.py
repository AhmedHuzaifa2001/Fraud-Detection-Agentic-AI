from langgraph.graph import StateGraph, START, END
from state.state import AgentState
from nodes.registrar_scout_node import registrar_scout_node
from nodes.geospatial_analyst_node import geospatial_analyst_node
from nodes.digital_footprint_node import digital_footprint_node
from nodes.supervisor_node import supervisor_node


workflow = StateGraph(AgentState)

## Adding the Nodes

workflow.add_node("registrar_scout_node" , registrar_scout_node)
workflow.add_node("geospatial_analyst_node" , geospatial_analyst_node)
workflow.add_node("digital_footprint_node" , digital_footprint_node)
workflow.add_node("supervisor_node" , supervisor_node)


## Adding Edges
workflow.add_edge(START , "registrar_scout_node")
workflow.add_edge("registrar_scout_node" , "geospatial_analyst_node")
workflow.add_edge("geospatial_analyst_node" , "digital_footprint_node")
workflow.add_edge("digital_footprint_node" , "supervisor_node")
workflow.add_edge("supervisor_node" , END)


graph_builder = workflow.compile()