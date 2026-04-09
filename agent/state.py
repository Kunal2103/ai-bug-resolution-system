from typing import TypedDict, Any

class GraphState(TypedDict):
    """The central state object passed between all agents in the graph."""
    bug_report_path: str
    logs_path: str
    triage_summary: str
    log_evidence: str
    repro_script_path: str
    repro_execution_result: str
    fix_plan: str
    final_report: Any
    dependency_analysis: str
    relevant_files_context: str