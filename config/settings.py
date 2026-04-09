import yaml
import os
from pathlib import Path
from utils.file_helpers import load_yaml_config

# Get the absolute path of the project root
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
CONFIG_FILE_PATH = os.path.join(PROJECT_ROOT, "config", "config.yaml")

def load_config(file_path=CONFIG_FILE_PATH):
    """Loads the YAML configuration file."""
    try:
            config = load_yaml_config(file_path)
            
            # Convert relative paths to absolute paths dynamically
            config['artifacts']['inputs']['bug_report'] = os.path.join(PROJECT_ROOT, config['artifacts']['inputs']['bug_report'])
            config['artifacts']['inputs']['logs'] = os.path.join(PROJECT_ROOT, config['artifacts']['inputs']['logs'])
            config['artifacts']['outputs']['final_report'] = os.path.join(PROJECT_ROOT, config['artifacts']['outputs']['final_report'])
            config['artifacts']['outputs']['repro_script'] = os.path.join(PROJECT_ROOT, config['artifacts']['outputs']['repro_script'])
            
            return config
    except Exception as e:
        raise Exception(f"Error loading config file: {e}")

# Global configuration dictionary
CONFIG = load_config()