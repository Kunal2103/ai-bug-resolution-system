# test/test_tools.py
import os
import pytest
# Assuming your functions are named read_file and write_file
from tools.file_tools import read_file, write_file 

def test_file_read_write_tools(tmp_path):
    """
    Test that our agent's file tools can successfully read and write.
    Uses pytest's built-in tmp_path to avoid leaving junk files on the hard drive.
    """
    # 1. Setup a temporary fake file path
    test_file = tmp_path / "dummy_script.py"
    test_content = "print('Hello, AI Bug Resolver!')"

    # 2. Test the Agent's Write Tool
    write_response = write_file.func(str(test_file), test_content)
    assert "Successfully" in write_response or "wrote" in write_response.lower()
    assert test_file.exists(), "The tool failed to create the file!"

    # 3. Test the Agent's Read Tool
    read_content = read_file.func(str(test_file))
    assert read_content == test_content, "The read tool altered the file contents!"