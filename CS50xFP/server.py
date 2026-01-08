"""
An easy way to run the server in utils

Executes the server with `python -m utils.server.main`
"""

import sys
import subprocess
from pathlib import Path

# Get project root (CS50xFP)
project_root = Path(__file__).parent

subprocess.run(
    [sys.executable, '-m', 'utils.server.main'],
    cwd=project_root
)
