import sys
import os
from config.settings import CONFIG
from logger import logger
from exception import CustomException
from agent.graph import get_resolution_app

def run_end_to_end():
    try:
        logger.info("🔥 Launching End-to-End Bug Resolution System — Bugs Beware!\n")

        resolution_app = get_resolution_app()
        
        # 1. Ensure output directories exist
        os.makedirs("data/outputs", exist_ok=True)
        
        # 2. Define the Initial State dynamically from our config
        initial_state = {
            "bug_report_path": CONFIG['artifacts']['inputs']['bug_report'],
            "logs_path": CONFIG['artifacts']['inputs']['logs'],
            "triage_summary": "",
            "dependency_analysis": "",
            "relevant_files_context": "",
            "log_evidence": "",
            "repro_script_path": "",
            "repro_execution_result": "",
            "fix_plan": "",
            "final_report": None
        }
        
        # 3. Execute the Graph
        logger.info("Invoking LangGraph workflow... (This may take some time.....)")
        final_state = resolution_app.invoke(initial_state)
        
        # 4. Extract and Save the Final Structured Output (Assessment Requirement)
        logger.info("Workflow complete. Extracting final report...\n")
        report_pydantic = final_state["final_report"]
        
        output_path = CONFIG['artifacts']['outputs']['final_report']
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_pydantic.model_dump_json(indent=2))
            
        logger.info(f"<<<----- SUCCESS! Final report saved to {output_path} ----->>>")
        
        # 5. Print a beautiful summary to the terminal for your demo video
        print("\n" + "="*100)
        print("🚀 MULTI-AGENT BUG RESOLUTION COMPLETE 🚀")
        print("="*100)
        print(f"Bug Summary: {report_pydantic.bug_summary}")
        print(f"Root Cause Hypothesis: {report_pydantic.root_cause_hypothesis}")
        print(f"\nArtifacts Generated:")
        print(f"  Repro Script: {final_state['repro_script_path']}")
        print(f"  Final Report: {output_path}")
        print("="*100 + "\n")
        
    except Exception as e:
        raise CustomException(e, sys)

if __name__ == "__main__":
    try:
        run_end_to_end()
    except CustomException as ce:
        print(f"\n--- System Failure ---\n{ce}")