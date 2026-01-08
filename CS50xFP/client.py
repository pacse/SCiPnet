"""
An easy way to run the client in utils

Executes the client with `python -m utils.client.main`
"""

import sys
import subprocess
from pathlib import Path

# Get project root (CS50xFP)
project_root = Path(__file__).parent

subprocess.run(
    [sys.executable, '-m', 'utils.client.main'],
    cwd=project_root
)
