import subprocess
import sys
import os
from langchain_core.tools import tool
from logger import logger
from exception import CustomException
from config.settings import CONFIG  

@tool
def execute_python_script(script_path: str) -> str:
    """
    Executes a given python script and returns its stdout and stderr.
    Useful for running reproduction tests to verify if a bug exists.
    """
    try:
        logger.info(f"Tool 'execute_python_script' called for script: {script_path}")
        if not os.path.exists(script_path):
            return f"Execution Error: Script '{script_path}' not found."
        
        timeout_limit = CONFIG.get('system_config', {}).get('timeout_seconds', 30)

        # Run the script with a timeout to prevent infinite loops
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=timeout_limit 
        )
        
        output = []
        output.append(f"Exit Code: {result.returncode}")
        if result.stdout:
            output.append(f"--- STDOUT ---\n{result.stdout}")
        if result.stderr:
            output.append(f"--- STDERR ---\n{result.stderr}")
            
        return "\n".join(output)
        
    except subprocess.TimeoutExpired:
        logger.warning(f"Execution of {script_path} timed out.")
        return "Execution Error: Script timed out after 30 seconds."
    except Exception as e:
        raise CustomException(e, sys)