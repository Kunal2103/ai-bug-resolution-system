from .file_tools import read_file, search_logs, write_file
from .execution_tools import execute_python_script

# Group all available tools in a list for our agents
AVAILABLE_TOOLS = [read_file, write_file, search_logs, execute_python_script]