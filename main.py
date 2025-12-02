"""Entry point for SQL agent CLI."""

import sys
from pathlib import Path

# Add src directory to path for development
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from sql_agent.cli import cli

if __name__ == "__main__":
    cli()
