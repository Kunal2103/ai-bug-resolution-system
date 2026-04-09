# utils/file_helpers.py
import yaml
import os
from exception import CustomException
from logger import logger

def load_yaml_config(file_path: str) -> dict:
    """Utility function to safely load a YAML configuration file."""
    if not os.path.exists(file_path):
        logger.error(f"Configuration file missing at: {file_path}")
        raise CustomException(f"File not found: {file_path}")
        
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Error parsing YAML file: {e}")
        raise CustomException(e)