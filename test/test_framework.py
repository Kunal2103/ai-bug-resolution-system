# test/test_framework.py
import os
import pytest
from utils.file_helpers import load_yaml_config
from dotenv import load_dotenv

load_dotenv()

def test_environment_variables():
    """Test that critical environment variables exist."""
    # Assuming you are using Groq, we ensure the key is loaded in the environment
    assert os.environ.get("GROQ_API_KEY") is not None, "GROQ_API_KEY is missing!"

def test_yaml_loader_handles_missing_file():
    """Test that our utility properly catches missing files."""
    with pytest.raises(Exception):
        load_yaml_config("dummy_path/that/does_not_exist.yaml")