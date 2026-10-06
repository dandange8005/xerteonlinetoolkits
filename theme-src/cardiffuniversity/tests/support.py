"""Shared paths for the theme's unit tests. Importing this puts tools/ on the import path."""
import importlib.util
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
THEME = TESTS.parent  # theme-src/cardiffuniversity
REPO = THEME.parents[1]
TOOLS = THEME / "tools"
GUIDE = THEME / "guide"

if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))


def load_tool(name):
    """Import a hyphen-named script in tools/, such as build-guide.py."""
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), TOOLS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
