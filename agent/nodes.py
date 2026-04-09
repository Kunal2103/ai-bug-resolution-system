import sys
from logger import logger
from exception import CustomException
from agent.state import GraphState
from agent.base import execute_agent
from tools.file_tools import read_file, search_logs, write_file,list_directories
from tools.execution_tools import execute_python_script
from prompt_library.prompts import (
    TRIAGE_AGENT_PROMPT, LOG_ANALYST_AGENT_PROMPT,
    REPRODUCTION_AGENT_PROMPT, FIX_PLANNER_AGENT_PROMPT,
    REVIEWER_AGENT_PROMPT,DEPENDENCY_ANALYST_PROMPT, REPO_NAVIGATOR_PROMPT
)
from prompt_library.schemas import BugResolutionReport
from config.settings import CONFIG

def triage_node(state: GraphState) -> GraphState:
    try:
        user_content = f"Read the bug report located at: {state['bug_report_path']}"
        result = execute_agent("Triage_Agent", TRIAGE_AGENT_PROMPT, user_content, tools=[read_file])
        state["triage_summary"] = result
        return state
    except Exception as e: raise CustomException(e, sys)

def log_analyst_node(state: GraphState) -> GraphState:
    try:
        user_content = (
            f"Triage Info: {state['triage_summary']}\n"
            f"Relevant Code Files Found: {state['relevant_files_context']}\n"
            f"Search the logs at {state['logs_path']} to find evidence of the bug."
        )
        result = execute_agent("Log_Analyst_Agent", LOG_ANALYST_AGENT_PROMPT, user_content, tools=[search_logs])
        state["log_evidence"] = result
        return state
    except Exception as e: raise CustomException(e, sys)
    
def reproduction_node(state: GraphState) -> GraphState:
    try:
        repro_path = CONFIG['artifacts']['outputs']['repro_script']
        user_content = (
            f"Triage: {state['triage_summary']}\nEvidence: {state['log_evidence']}\n"
            f"Write a minimal python reproduction script to {repro_path} using your write_file tool. "
            f"Then, execute it using your execute_python_script tool."
        )
        result = execute_agent("Reproduction_Agent", REPRODUCTION_AGENT_PROMPT, user_content, tools=[write_file, execute_python_script])
        state["repro_script_path"] = repro_path
        state["repro_execution_result"] = result
        return state
    except Exception as e: raise CustomException(e, sys)

def fix_planner_node(state: GraphState) -> GraphState:
    try:
        user_content = (
            f"Triage: {state['triage_summary']}\n"
            f"Evidence: {state['log_evidence']}\n"
            f"Repro Result: {state['repro_execution_result']}\n"
            "Propose a detailed patch plan. If you need to verify the source code, use the read_file tool."
        )
        result = execute_agent("Fix_Planner_Agent", FIX_PLANNER_AGENT_PROMPT, user_content, tools=[read_file])
        state["fix_plan"] = result
        return state
    except Exception as e: raise CustomException(e, sys)

def reviewer_node(state: GraphState) -> GraphState:
    try:
        user_content = (
            f"Triage: {state['triage_summary']}\n"
            f"Evidence: {state['log_evidence']}\n"
            f"Fix Plan: {state['fix_plan']}\n"
            "Review the plan and generate the final BugResolutionReport. Ensure it matches the structured schema."
        )
        result = execute_agent("Reviewer_Agent", REVIEWER_AGENT_PROMPT, user_content, tools=[read_file], structured_output=BugResolutionReport)
        state["final_report"] = result
        return state
    except Exception as e: raise CustomException(e, sys)


def dependency_analyst_node(state: GraphState) -> GraphState:
    try:
        user_content = f"Triage Info: {state['triage_summary']}\nCheck the root directory for dependency files and analyze them."
        result = execute_agent("Dependency_Analyst_Agent", DEPENDENCY_ANALYST_PROMPT, user_content, tools=[read_file])
        state["dependency_analysis"] = result
        return state
    except Exception as e: raise CustomException(e, sys)


def repo_navigator_node(state: GraphState) -> GraphState:
    try:
        user_content = (
            f"Triage Info: {state['triage_summary']}\n"
            f"Dependency Findings: {state['dependency_analysis']}\n"
            "Search the directory and find the specific Python files related to this bug."
        )
        result = execute_agent("Repo_Navigator_Agent", REPO_NAVIGATOR_PROMPT, user_content, tools=[list_directories, read_file])
        state["relevant_files_context"] = result
        logger.info(f"[Repo_Navigator_Agent] 🎯 Target File Successfully Identified:{result}\n")
        
        return state
    except Exception as e: raise CustomException(e, sys)