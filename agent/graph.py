import sys
from langgraph.graph import StateGraph, START, END
from logger import logger
from exception import CustomException
from agent.state import GraphState
from agent.nodes import (
    triage_node, 
    log_analyst_node, 
    reproduction_node, 
    fix_planner_node, 
    reviewer_node,
    dependency_analyst_node, repo_navigator_node
)

def build_resolution_graph():
    """Compiles the deterministic multi-agent workflow."""
    try:
        logger.info("Building the LangGraph workflow...")
        
        # Initialize the graph with our state schema
        workflow = StateGraph(GraphState)

        # 1. Define the Nodes (The Agents)
        workflow.add_node("Triage", triage_node)
        workflow.add_node("Dependency_Analyst", dependency_analyst_node)
        workflow.add_node("Repo_Navigator", repo_navigator_node)
        workflow.add_node("Log_Analyst", log_analyst_node)
        workflow.add_node("Reproduction", reproduction_node)
        workflow.add_node("Fix_Planner", fix_planner_node)
        workflow.add_node("Reviewer", reviewer_node)

        # 2. Define the Edges (The strict, deterministic workflow)
        workflow.add_edge(START, "Triage")
        workflow.add_edge("Triage", "Dependency_Analyst")
        workflow.add_edge("Dependency_Analyst", "Repo_Navigator")
        workflow.add_edge("Repo_Navigator", "Log_Analyst")
        workflow.add_edge("Log_Analyst", "Reproduction")
        workflow.add_edge("Reproduction", "Fix_Planner")
        workflow.add_edge("Fix_Planner", "Reviewer")
        workflow.add_edge("Reviewer", END)

        # 3. Compile the graph
        app = workflow.compile()
        logger.info("Graph compiled successfully.")
        return app
        
    except Exception as e:
        raise CustomException(e, sys)

#  initialization of compiled LangGraph workflow
def get_resolution_app():
    return build_resolution_graph()