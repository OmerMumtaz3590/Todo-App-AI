"""Todo List Application - Phase I

A simple in-memory todo list console application.
All data is lost when the application exits.

Usage:
    python -m src.main

Spec Reference: FR-010 (clean exit), NFR-001 (single-user console app)
Plan Reference: main.py
"""

import sys
from pathlib import Path

# If the module is executed directly from the `src` folder (not as a package),
# ensure the project root (parent of `src`) is on `sys.path` so `src` can be
# imported as a package. This makes running `python main.py` or tools that
# execute the script from `src` work correctly.
if __package__ is None:
    _current = Path(__file__).resolve()
    _project_root = str(_current.parent.parent)
    if _project_root not in sys.path:
        sys.path.insert(0, _project_root)

from src.cli import TodoMenu


def main() -> None:
    """Run the todo list application."""
    menu = TodoMenu()
    menu.run()


if __name__ == "__main__":
    main()
